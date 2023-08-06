#!/usr/bin/env python
"""Copy workflow app."""
import os
import sys
import logging

from ruffus import *

from applicake.apps.examples.cp import CpApp
from applicake.apps.flow.merge import Merge
from applicake.apps.flow.split import Split
from applicake.base import Argument, Keys, KeyHelp, BasicApp
from applicake.base.coreutils import IniInfoHandler


@split("input.ini", "split.ini_*")
def split(infile, unused_outfile):
    sys.argv = ['--INPUT', infile, '--SPLIT', 'split.ini', '--SPLIT_KEY', 'FILE']
    Split.main()

@transform(split, regex("split.ini_"), "echo.ini_")
def echo(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    CpApp.main()

@merge(echo, "merged.ini")
def merge(unused_infile, outfile):
    sys.argv = ['--MERGE', 'echo.ini', '--MERGED', outfile]
    Merge.main()


class CopyWorkflow(BasicApp):
    """Let's wrap a ruffus workflow in an app."""

    def add_args(self):
        return [
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument("FILE", "FILE FOR COPY JOB"),
            Argument(Keys.THREADS, KeyHelp.THREADS, default=1),
        ]

    def run(self, info):
        #write ini for workflow, contains BASEDIR + JOBID
        pipeline_info = info.copy()

        path = os.path.join(pipeline_info["WORKDIR"], "input.ini")
        IniInfoHandler().write(info, path)

        #run workflow
        os.chdir(pipeline_info['BASEDIR'])
        pipeline_run([merge], multiprocess=int(pipeline_info[Keys.THREADS]))

        #parse "important information"
        pipeline_info = IniInfoHandler().read("merged.ini_0")
        pipeline_info['BASEDIR'] = info['BASEDIR']

        info = pipeline_info
        logging.debug("NOW THIS IS THE REAL RESULT. I FETCHED FROM SUBWORKFLOW %s" % info['COPY'])

        return info

#use this class as executable
if __name__ == "__main__":
    CopyWorkflow.main()
