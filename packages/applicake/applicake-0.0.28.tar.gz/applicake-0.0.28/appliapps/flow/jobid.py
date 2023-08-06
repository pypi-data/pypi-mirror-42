#!/usr/bin/env python
"""Jobid appliapp."""

from applicake.base import BasicApp, Argument, Keys, KeyHelp


class Jobid(BasicApp):
    """creates empty workdir, sometimes needed as init node for setting JOB_ID."""

    def add_args(self):
        return [
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR)
        ]

    def run(self, info):
        return info


if __name__ == "__main__":
    Jobid.main()
