#!/usr/bin/env python
"""Branching appliapp."""
import logging
from applicake.base import BasicApp
from applicake.base.coreutils import Argument
from applicake.base.coreutils.info import get_handler
from applicake.base.coreutils import Keys, KeyHelp


class Branch(BasicApp):
    """Braching appliapp."""
    def add_args(self):
        return [
            Argument(Keys.ALL_ARGS, KeyHelp.ALL_ARGS),
            Argument(Keys.BRANCH, KeyHelp.BRANCH)
        ]

    def run(self, info):
        infoh = get_handler(info[Keys.BRANCH])
        tobranch = info[Keys.BRANCH].split(" ")
        del info[Keys.BRANCH]
        for branch in tobranch:
            logging.info("Branching %s", branch)
            info = info.copy()
            infoh.write(info, branch)

        return info


if __name__ == "__main__":
    Branch.main()
