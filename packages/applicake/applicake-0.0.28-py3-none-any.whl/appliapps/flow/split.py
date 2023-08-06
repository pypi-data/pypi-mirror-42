#!/usr/bin/env python
"""Split appliapp."""
import copy
import logging

from applicake.base.coreutils.arguments import Argument
from applicake.base.coreutils.info import get_handler
from applicake.base.app import BasicApp
from applicake.base.coreutils.keys import Keys, KeyHelp


class Split(BasicApp):
    """Split appliapp."""
    def add_args(self):
        return [
            Argument(Keys.ALL_ARGS, KeyHelp.ALL_ARGS),
            Argument(Keys.SPLIT, KeyHelp.SPLIT),
            Argument(Keys.SPLIT_KEY, KeyHelp.SPLIT_KEY)
        ]

    def run(self, info):
        basename = info[Keys.SPLIT]
        key = info[Keys.SPLIT_KEY]
        value = info.get(key, "")
        if not isinstance(value, list):
            value = [value]

        info = info.copy()
        del info[Keys.SPLIT]
        del info[Keys.SPLIT_KEY]

        if info.get(Keys.SUBJOBLIST, "") == "":
            info[Keys.SUBJOBLIST] = []

        for i, val in enumerate(value):
            infocopy = copy.deepcopy(info)
            infocopy[key] = val
            infocopy[Keys.SUBJOBLIST].append("%s%s%d%s%d" % (key, Keys.SUBJOBSEP, i, \
                                             Keys.SUBJOBSEP, len(value)))
            path = basename + "_" + str(i)
            logging.debug("Writing split file %s", path)
            get_handler(basename).write(infocopy, path)

        return info


if __name__ == "__main__":
    Split.main()
