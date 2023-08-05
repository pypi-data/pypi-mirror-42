##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


from build.transform import pybuild
from build.tools import Tool
import platform
from os import path


class Directory(pybuild.Command):
    def __init__(self, dirname):
        ignore_error = False
        if platform.system() == "Windows":
            cmdline = "cmd /c if not exist \"{dir}\" mkdir \"{dir}\"".format(dir=dirname)
            ignore_error = True
        else:
            cmdline = "mkdir -p \"{dir}\"".format(dir=dirname)
        info = ' [MKDIR] {}'.format(dirname)
        super(Directory, self).__init__(dirname, cmdline, info, ignore_error=ignore_error)

    @property
    def required(self):
        return not path.exists(self.product)

    @property
    def timestamp(self):
        return 0


class PyBuildDirectoryCreator(Tool):
    def __init__(self):
        super(PyBuildDirectoryCreator, self).__init__()

    def transform(self, cxx_project, dirname):
        job = cxx_project.get_job(dirname)
        if not job:
            job = Directory(dirname)
            cxx_project.add_job(job)
        return job
