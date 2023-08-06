"""utils to support directories."""
import errno
import os
import re
import shutil
import time
import logging

from applicake.base.coreutils import Keys


def create_workdir(info):
    """Create the workdir."""
    if not Keys.WORKDIR in info:
        logging.debug("No WORKDIR requested")
        return info

    if info[Keys.WORKDIR] != "":
        logging.debug("Using specified WORKDIR [%s]", info[Keys.WORKDIR])
        return info

    # No workdir specified, creating one using BASEDIR, JOB_IDX, SUBJOBLIST, NAME
    if info.get(Keys.JOB_ID, "") == "":
        info[Keys.JOB_ID] = create_unique_jobdir(info[Keys.BASEDIR])
        logging.debug("JOB_ID was not set, generated [%s]", info[Keys.JOB_ID])

    workdir = ''
    for key in [Keys.BASEDIR, Keys.JOB_ID]:
        if key in info:
            workdir += info[key] + os.path.sep

    if info.get(Keys.SUBJOBLIST, "") != "":
        if not isinstance(info[Keys.SUBJOBLIST], list):
            info[Keys.SUBJOBLIST] = [info[Keys.SUBJOBLIST]]
        for subjob in info[Keys.SUBJOBLIST]:
            dataset = re.sub(r"\W", "", subjob.split(Keys.SUBJOBSEP)[0]) + '_' \
                             + subjob.split(Keys.SUBJOBSEP)[1]
            workdir += dataset + os.path.sep

    workdir += info[Keys.NAME] + os.path.sep
    makedirs_clean(workdir)
    logging.debug("Created WORKDIR [%s]", workdir)
    info[Keys.WORKDIR] = workdir

    return info


def create_unique_jobdir(basedir):
    """Creates a unique job directory."""
    # dirname using timestamp, principle from tempfile.mkdtemp()
    #limits: longer foldername if >1 dir/min error on >1000 dir/min
    dirname = time.strftime("%y%m%d%H%M")
    ext = ""
    for i in range(0, 1000):
        try:
            path = os.path.join(basedir, dirname + ext)
            os.mkdir(path)
            os.chmod(path, 0o775)
            return dirname + ext
        except OSError as error:
            if error.errno == errno.EEXIST:
                ext = '-' + str(i)
                continue  # try again
            raise
    raise Exception("Could not create a unique job directory")


def makedirs_clean(workdir):
    """like os.makedirs(dir) but cleans lowest folder"""
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    makedirs_chmod(workdir)


def makedirs_chmod(newdir, mode=0o775):
    """like os.makedirs(dir,mode) but chmod of ALL created subfolders"""
    head, tail = os.path.split(newdir)
    if head and not os.path.isdir(head):
        makedirs_chmod(head)
    if tail:
        os.mkdir(newdir)
        os.chmod(newdir, mode)
