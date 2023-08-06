"""The main applicake app module."""
import os
import subprocess
import sys
import time
import getpass
import re
import logging

from applicake.base.apputils import dirs
from applicake.base.apputils import dicts
from applicake.base.apputils import validation
from applicake.base.coreutils.keys import Keys, KeyHelp
from applicake.base.coreutils.arguments import Argument, parse_sysargs
from applicake.base.coreutils.info import get_handler


class IApp:
    """IApp - The App Base class."""
    @classmethod
    def main(cls):
        """
        Main method to run through the whole App

        @return : None
        """
        raise NotImplementedError

    def add_args(self):
        """
        Defines Arguments required or used by App

        @return: list with Arguments
        """
        raise NotImplementedError

    def setup(self, app_args):
        """
        Set up environment for running App

        @param app_args: Arguments required by App
        @return: dict with info
        """
        raise NotImplementedError

    def run(self, info):
        """
        Run the App

        @param info: dict with info
        @return: (modified) dict with info
        """
        raise NotImplementedError

    def teardown(self, info):
        """
        Clean up enviroment after running App

        @param info: dict with info
        @return: None
        """
        raise NotImplementedError


class BasicApp(IApp):
    """BasicApp - for python code."""
    @classmethod
    def main(cls):
        try:
            start = time.time()
            clsi = cls()
            app_args = clsi.add_args()
            req_info, info = clsi.setup(app_args)
            ret_info = clsi.run(req_info)
            info = dicts.merge(info, ret_info, priority='right')

            clsi.teardown(info)
            logging.debug("%s finished successfully at %s", cls.__name__, time.asctime())
            logging.info("%s finished successfully (%ss)", cls.__name__, int(time.time() - start))
        except RuntimeError as error:
            msg = cls.__name__ + " failed! " + str(error)
            if isinstance(error, KeyError):
                msg += " key not found in info"
            msg += "\n"
            # feature request cuklinaj: mail when fail, delay between
            if os.environ.get("LSB_JOBID"):
                controlfile = os.getenv("HOME") + "/.last_error_message"
                if not os.path.exists(controlfile) or\
                   (time.time() - os.stat(controlfile).st_mtime) > 300:
                    subprocess.call("touch %s; echo \"Failure reason: %s\" | \
                                     mail -s \"Workflow Failed\" %s" % (
                                         controlfile, msg, getpass.getuser()), shell=True)
            logging.error(msg)
            sys.exit(1)

    def add_args(self):
        raise NotImplementedError("add_args() not implemented")

    def setup(self, app_args):
        # basic arguments for every node
        basic_args = [Argument(Keys.INPUT, KeyHelp.INPUT, default=''),
                      Argument(Keys.OUTPUT, KeyHelp.OUTPUT, default=''),
                      Argument(Keys.MODULE, KeyHelp.MODULE, default=''),
                      Argument(Keys.LOG_LEVEL, KeyHelp.LOG_LEVEL, default="INFO")]

        # WORKDIR: if WORKDIR is defined add related args
        for i, arg in enumerate(app_args):
            if arg.name == Keys.WORKDIR:
                app_args.insert(i + 1, Argument(Keys.BASEDIR, KeyHelp.BASEDIR, default='.'))
                app_args.insert(i + 2, Argument(Keys.JOB_ID, KeyHelp.JOB_ID, default=''))
                app_args.insert(i + 3, Argument(Keys.SUBJOBLIST, KeyHelp.SUBJOBLIST, default=''))
                app_args.insert(i + 4, Argument(Keys.NAME, KeyHelp.NAME,
                                                default=self.__class__.__name__))
                break

        defaults, cliargs = parse_sysargs(basic_args + app_args)

        # construct info from defaults < info < commandlineargs
        infh = get_handler(cliargs.get(Keys.INPUT, None))
        fileinfo = infh.read(cliargs.get(Keys.INPUT, None))
        info = dicts.merge(cliargs, dicts.merge(fileinfo, defaults))

        # request by malars: show dataset prominent in logger
        if Keys.DATASET_CODE in info:
            if not isinstance(info[Keys.DATASET_CODE], list):
                if Keys.MZXML in info and not isinstance(info[Keys.MZXML], list):
                    logging.info("Dataset is %s (%s)",
                                 info[Keys.DATASET_CODE],
                                 os.path.basename(info[Keys.MZXML]))
                else:
                    logging.info("Dataset is %s", info[Keys.DATASET_CODE])
            else:
                logging.debug("Datasets are %s", info[Keys.DATASET_CODE])

        # WORKDIR: create WORKDIR (only after mk)
        info = dirs.create_workdir(info)

        # filter to requested args
        if Keys.ALL_ARGS in info:
            # if ALL_ARGS is set give whole info to app...
            req_info = info
        else:
            req_info = {}
            # ...otherwise copy only explicitly requested args to app
            for key in [arg.name for arg in basic_args + app_args]:
                if key in info:
                    req_info[key] = info[key]
        logging.debug("info for app: %s", req_info)
        return req_info, info

    def run(self, info):
        raise NotImplementedError("run() not implemented")

    def teardown(self, info):
        infh = get_handler(info.get(Keys.OUTPUT))
        infh.write(info, info.get(Keys.OUTPUT))


class WrappedApp(BasicApp):
    """WrappedApp - for executing command line tools."""
    def run(self, info):
        info, cmd = self.prepare_run(info)
        exit_code, stdout = self.execute_run(info, cmd)
        info = self.validate_run(info, exit_code, stdout)
        return info

    def prepare_run(self, info):
        """prepare_run method, not implemented in base class."""
        raise NotImplementedError("prepare_run() not implemented")

    def execute_run(self, info, cmd):
        """Default execute run method."""
        out = ""
        exit_code = 0
        if isinstance(cmd, list):
            for single_command in cmd:
                exit_code_s, out_s = self.execute_run_single(info, single_command)
                exit_code += exit_code
                out += out_s
                if exit_code_s != 0:
                    break
        else:
            exit_code, out = self.execute_run_single(info, cmd)
        return exit_code, out

    @staticmethod
    def execute_run_single(info, cmd):
        """Execute a single run."""
        # feature request lgillet: append all executed commands to inifile, shorten paths
        info['COMMAND_HISTORY'] = str(info.get('COMMAND_HISTORY', "")) + \
                                  re.sub(r"/[^ ]*/([^ ]*) ", r"\1 ", cmd.strip())+"; "
        # if MODULE is set load specific module before running cmd.
        # requires http://modules.sourceforge.net/
        if info.get('MODULE', '') != '':
            cmd = "module purge && module load %s && %s" % (info['MODULE'], cmd)

        cmd = cmd.strip()
        logging.debug("command is [%s]", cmd)
        # stderr to stdout: http://docs.python.org/2/library/subprocess.html#subprocess.STDOUT
        # read input "streaming" from subprocess: http://stackoverflow.com/a/17698359
        # get exitcode: http://docs.python.org/2/library/subprocess.html#subprocess.Popen.returncode
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, bufsize=1)
#        out = ""
#        for line in iter(proc.stdout.readline, ''):
#            print(line.strip())
#            out += line
        out, _ = proc.communicate()
        out = out.decode('utf-8')
        print(out)
        exit_code = proc.returncode
        return exit_code, out

    @classmethod
    def validate_run(cls, info, exit_code, stdout):
        """Validate the run."""
        validation.check_exitcode(exit_code)
        validation.check_stdout(stdout)
        return info
