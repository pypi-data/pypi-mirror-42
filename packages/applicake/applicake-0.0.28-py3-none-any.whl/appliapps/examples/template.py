#!/usr/bin/env python
"""Applicake templating."""
import os
import logging

from applicake.base.app import BasicApp
from applicake.base.apputils.dirs import create_workdir
from applicake.base.coreutils import Argument
from applicake.base.apputils import templates
from applicake.base.coreutils import Keys, KeyHelp


class TemplateApp(BasicApp):
    """
    A more advanced example for a BasicApp
    performing template reading, modifying and writing
    """

    def add_args(self):
        return [
            Argument("COMMENT", "value for comment variable"),
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR)
        ]

    def run(self, info):
        info = create_workdir(info)

        info['TEMPLATEFILE'] = os.path.join(info[Keys.WORKDIR], "template_out.tpl")
        templates.read_mod_write(info, templates.get_tpl_of_class(self), info['TEMPLATEFILE'])
        logging.debug("Templatefile sucessfully written. Contents are [%s]", \
                      open(info['TEMPLATEFILE']).read())

        return info


if __name__ == "__main__":
    TemplateApp.main()
