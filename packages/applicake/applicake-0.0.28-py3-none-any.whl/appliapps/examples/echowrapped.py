#!/usr/bin/env python
"""basic example of a WrappedApp"""
import logging
from applicake.base import WrappedApp
from applicake.base.coreutils import Argument
from applicake.base.coreutils import Keys, KeyHelp


class EchoWrapped(WrappedApp):
    """
    A most simple example for a WrappedApp
    prints COMMENT to stdout using '/bin/echo'

    Note: validate run not overwritten here because default is OK
    """

    def add_args(self):
        return [
            Argument(Keys.EXECUTABLE, KeyHelp.EXECUTABLE, default="echo"),
            Argument("COMMENT", "String to be displayed", default="default comment")
        ]

    def prepare_run(self, info):
        exe = info["EXECUTABLE"]
        comment = info["COMMENT"]
        command = "%s %s" % (exe, comment)
        logging.debug("Executable is %s", exe)
        logging.info("Comment is %s", comment)
        return info, command

#use this class as executable
if __name__ == "__main__":
    EchoWrapped.main()
