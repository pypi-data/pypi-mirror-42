#!/usr/bin/env python
"""App to collate dictionaries."""
import logging
import applicake.base.apputils.dicts as dicts
from applicake.base.coreutils import Argument
from applicake.base.coreutils.info import get_handler
from applicake.base import BasicApp
from applicake.base.coreutils import Keys, KeyHelp


class Collate(BasicApp):
    """Collate appliapp."""
    def add_args(self):
        return [
            Argument(Keys.ALL_ARGS, KeyHelp.ALL_ARGS),
            Argument(Keys.COLLATE, KeyHelp.COLLATE)
        ]

    def run(self, info):
        infoh = get_handler(info[Keys.COLLATE])
        paths = info[Keys.COLLATE].split(" ")
        del info[Keys.COLLATE]
        collector_config = info.copy()

        #read in
        for path in paths:
            logging.debug('collating file [%s]', path)
            config = infoh.read(path)
            collector_config = dicts.merge(collector_config, config, priority='append')

        #unify
        for key in collector_config.keys():
            collector_config[key] = dicts.unify(collector_config[key])

        #write back
        return collector_config


if __name__ == "__main__":
    Collate.main()
