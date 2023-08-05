import keyring
import sys
import getpass
import inspect
import hashlib
from jinja2 import Template
import time
from requests.exceptions import ConnectionError, ReadTimeout

from jolt import config
from jolt import utils
from jolt import scheduler
from jolt.tps.jenkins import Jenkins
from jolt import log
from jolt import loader
from jolt import filesystem as fs

NAME = "jenkins"
TYPE = "Remote execution"
TIMEOUT = (3.5, 27)


@utils.Singleton
class JenkinsServer(object):
    def __init__(self):
        username, password = self._get_auth()
        self._server = Jenkins(config.get(NAME, "uri"), username, password, timeout=TIMEOUT)
        self.get_job_info = self._server.get_job_info
        self.get_build_info = self._server.get_build_info
        self.get_build_console_output = self._server.get_build_console_output
        self.get_queue_item = self._server.get_queue_item
        self.build_job = self._server.build_job
        self.stop_build = self._server.stop_build
        self.cancel_queue = self._server.cancel_queue
        try:
            self._ok = self._check_job()
        except:
            log.exception()
            log.warn("[JENKINS] failed to establish server connection, disabled")
            self._ok = False

    def _get_auth(self):
        service = config.get(NAME, "keyring.service")
        if not service:
            service = utils.read_input(NAME + " keyring service name (jenkins): ")
            if not service:
                service = NAME
            config.set(NAME, "keyring.service", service)
            config.save()

        username = config.get(NAME, "keyring.username")
        if not username:
            username = utils.read_input(NAME + " username: ")
            assert username, "no username configured for " + NAME
            config.set(NAME, "keyring.username", username)
            config.save()

        password = config.get(NAME, "keyring.password") or \
                   keyring.get_password(NAME, username)
        if not password:
            password = getpass.getpass(NAME + " password: ")
            assert password, "no password in keyring for " + NAME
            keyring.set_password(service, username, password)
        return username, password

    def _get_sha(self, data):
        sha = hashlib.sha1()
        sha.update(data.encode())
        return sha.hexdigest()

    def _get_job_template_path(self):
        default = fs.path.join(fs.path.dirname(__file__), "jenkins.job")
        return config.get(NAME, "template", default)

    def _load_job_template(self):
        with open(self._get_job_template_path()) as f:
            xml = f.read()
        return xml, self._get_sha(xml)

    def _check_job(self):
        template_xml, template_sha = self._load_job_template()
        self.job_name = "{0}-{1}".format(
            config.get(NAME, "job", "Jolt"),
            template_sha[:6])

        try:
            job_xml = self._get_job_config(self.job_name)
        except:
            self._create_job(self.job_name, template_xml, self._server.create_job)
            view = config.get(NAME, "view")
            if view:
                self._add_job_to_view(view, self.job_name)
            return True
        if self._get_sha(job_xml) != template_sha:
            assert self._create_job(
                self.job_name, template_xml, self._server.reconfig_job), \
                "[JENKINS] failed to change misconfigured job"
        return True

    def ok(self):
        return self._ok

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _create_job(self, name, job_template, func):
        template = Template(job_template)
        network_config = config.get("network", "config", "", expand=False)
        xml = template.render(config=network_config)
        func(name, xml)
        return True

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _add_job_to_view(self, view, job):
        self._server.add_job_to_view(view, job)

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _get_job_config(self, job):
        return self._server.get_job_config(job)


class JenkinsExecutor(scheduler.NetworkExecutor):
    def __init__(self, factory, task):
        super(JenkinsExecutor, self).__init__(factory)
        self.server = JenkinsServer.get()
        self.factory = factory
        self.task = task
        self.job = self.server.job_name

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _get_queue_item(self, queue_id):
        return self.server.get_queue_item(queue_id)

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _get_build_info(self, build_id):
        return self.server.get_build_info(self.job, build_id)

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _build_job(self, parameters):
        return self.server.build_job(self.job, parameters)

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _cancel_queue(self, queue_id):
        return self.server.cancel_queue(queue_id)

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _stop_build(self, build_id):
        return self.server.stop_build(self.job, build_id)

    @utils.retried.on_exception((ConnectionError, ReadTimeout))
    def _get_console_log(self, build_id):
        if not config.getboolean(NAME, "console", True):
            return
        logtext = self.server.get_build_console_output(self.job, build_id)
        for line in logtext.splitlines():
            if line.startswith("[ERROR]"):
                log.error(line[8:], log_context=self.task.identity[:8])
            elif line.startswith("[VERBOSE]"):
                log.verbose(line[10:], log_context=self.task.identity[:8])
            elif line.startswith("[HYSTERICAL]"):
                log.hysterical(line[13:], log_context=self.task.identity[:8])
            else:
                log.stdout(line, log_context=self.task.identity[:8])

    def _run(self, env):
        task = [self.task.qualified_name]
        task += [t.qualified_name for t in self.task.extensions]

        parameters = {
            "joltfile": loader.JoltLoader.get().get_sources(),
            "task": " ".join(task),
            "task_identity": self.task.identity[:8],
            "task_default": " ".join(["-d {0}".format(d) for d in self.factory.options.default])
        }
        parameters.update(scheduler.ExecutorRegistry.get().get_network_parameters(self.task))

        queue_id = self._build_job(parameters)

        log.verbose("[JENKINS] Queued {0}", self.task.qualified_name)

        queue_info = self._get_queue_item(queue_id)
        while not queue_info.get("executable"):
            assert not queue_info.get("cancelled"),\
            "[JENKINS] {0} failed with status CANCELLED".format(
                self.task.qualified_name)
            if self.is_aborted():
                self._cancel_queue(queue_id)
                assert False, "[JENKINS] execution cancelled"
            time.sleep(5)
            queue_info = self._get_queue_item(queue_id)

        log.verbose("[JENKINS] Executing {0}", self.task.qualified_name)

        build_id = queue_info["executable"]["number"]
        build_info = self._get_build_info(build_id)
        while build_info["result"] not in ["SUCCESS", "FAILURE", "ABORTED"]:
            if self.is_aborted():
                self._stop_build(build_id)
                assert False, "[JENKINS] execution cancelled"
            time.sleep(5)
            build_info = self._get_build_info(build_id)

        log.verbose("[JENKINS] Finished {0}", self.task.qualified_name)

        if build_info["result"] != "SUCCESS":
            self._get_console_log(build_id)

        assert build_info["result"] == "SUCCESS", \
            "[JENKINS] {1} failed with status {0}".format(
                build_info["result"], self.task.qualified_name)

        assert env.cache.is_available_remotely(self.task), \
            "[JENKINS] no artifact produced for {0}, check configuration"\
            .format(self.task.qualified_name)

        assert env.cache.download(self.task) or \
            not env.cache.download_enabled(), \
            "[JENKINS] failed to download artifact for {0}"\
            .format(self.task.qualified_name)

        for extension in self.task.extensions:
            assert env.cache.download(extension) or \
                not env.cache.download_enabled(), \
                "[JENKINS] failed to download artifact for {0}"\
                .format(extension.qualified_name)

        return self.task

    def run(self, env):
        try:
            self.task.started(TYPE)
            for extension in self.task.extensions:
                extension.started(TYPE)
            self._run(env)
            for extension in self.task.extensions:
                extension.finished(TYPE)
            self.task.finished(TYPE)
        except Exception as e:
            log.exception()
            for extension in self.task.extensions:
                extension.failed(TYPE)
            self.task.failed(TYPE)
            raise e
        return self.task


@scheduler.ExecutorFactory.Register
class JenkinsExecutorFactory(scheduler.NetworkExecutorFactory):
    def __init__(self, options):
        workers = config.get(NAME, "workers", 16)
        super(JenkinsExecutorFactory, self).__init__(max_workers=workers)
        self._options = options

    @property
    def options(self):
        return self._options

    def create(self, task):
        server = JenkinsServer.get()
        if not server.ok():
            return None
        return JenkinsExecutor(self, task)

log.verbose("Jenkins loaded")
