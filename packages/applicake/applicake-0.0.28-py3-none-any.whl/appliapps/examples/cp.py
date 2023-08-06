#!/usr/bin/env python
"""WrappedApp with validation."""
import os
import logging

from applicake.base.app import WrappedApp
from applicake.base.apputils.dirs import create_workdir
from applicake.base.apputils import validation
from applicake.base.coreutils import Argument
from applicake.base.coreutils import KeyHelp, Keys


class CpApp(WrappedApp):
    """
    A more advanced example for a WrappedApp
    copies FILE to COPY using 'cp', and implements own validation routine
    """

    def add_args(self):
        return [
            Argument(Keys.EXECUTABLE, KeyHelp.EXECUTABLE, default='cp'),
            Argument("FILE", "File to be copied"),
            Argument(Keys.WORKDIR, "folder where FILE will go into, created if not specified.")
        ]

    def prepare_run(self, info):
        info = create_workdir(info)
        info['COPY'] = os.path.join(info[Keys.WORKDIR], os.path.basename(info['FILE']))
        command = "%s %s %s" % (info['EXECUTABLE'], info["FILE"], info['COPY'])
        return info, command

    def validate_run(self, info, exit_code, stdout):
        logging.debug("Cp validation")
        #self checked
        if "No such file" in stdout:
            raise RuntimeError("Inputfile not found")

        if "Permission denied" in stdout:
            raise RuntimeError("Was not allowed to read inputfile. Need more rights")
        #validation util
        validation.check_file(info['COPY'])
        validation.check_exitcode(exit_code)
        return info

#use this class as executable
if __name__ == "__main__":
    CpApp.main()
