#!/usr/bin/env python
"""basic example of a BasicApp"""
from applicake.base import BasicApp
from applicake.base.coreutils import Argument
from applicake.base.coreutils import Keys, KeyHelp


class EchoBasic(BasicApp):
    """
    A most simple example for a BasicApp
    prints COMMENT to stdout
    """

    def add_args(self):
        return [
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument("COMMENT", "String to be displayed")
        ]

    def run(self, info):
        print(info["COMMENT"])
        return info

#use this class as executable
if __name__ == "__main__":
    EchoBasic.main()
