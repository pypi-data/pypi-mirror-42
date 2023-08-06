#!/usr/bin/env python
"""MergeToLine appliapp."""
import shutil

from applicake.base import BasicApp


class MergeToLine(BasicApp):
    """MergeToLine appliapp."""
    def add_args(self):
        pass

    def run(self, info):
        pass

    @classmethod
    def main(cls):
        #merges input.ini to one line (guse conditional execution check) and copies input to output
        merge = open('input.ini').read().replace('\n', '')
        print(merge)
        open('merge.ini', 'w').write(merge)
        shutil.copy("input.ini", "output.ini")
