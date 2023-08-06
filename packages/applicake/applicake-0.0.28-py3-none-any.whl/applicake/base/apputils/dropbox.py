"""Dropbox, prepare files to be imported into data manager."""
import os
import shutil
import subprocess
import logging

from applicake.base.apputils import dirs, validation
from applicake.base.coreutils import Keys


def get_experiment_code(info):
    """Return the experiment code."""
    #caveat: fails if no job_idx defined.
    uniq_exp_code = 'E' + info[Keys.JOB_ID]
    if info.get(Keys.SUBJOBLIST, "") != "":
        for subjob in info[Keys.SUBJOBLIST]:
            uniq_exp_code += "_" + subjob.split(Keys.SUBJOBSEP)[1]

    return uniq_exp_code

def make_stagebox(info):
    """Make a temporary folder to stage files."""
    dirname = ""
    if 'SPACE' in info:
        dirname += info['SPACE'] + "+"
    if 'PROJECT' in info:
        dirname += info['PROJECT'] + "+"
    dirname += get_experiment_code(info)
    dirname = os.path.join(info[Keys.WORKDIR], dirname)
    logging.debug("stagebox is %s", dirname)
    dirs.makedirs_clean(dirname)
    return dirname


def keys_to_dropbox(info, keys, tgt):
    """Add entries stored in info."""
    if not isinstance(keys, list):
        keys = [keys]
    for key in keys:
        if not key in info:
            raise Exception('key [%s] not found in info for copying to dropbox' % key)
        if isinstance(info[key], list):
            files = info[key]
        else:
            files = [info[key]]
        for filename in files:
            try:
                logging.debug('Copy [%s] to [%s]', filename, tgt)
                shutil.copy(filename, tgt)
            except RuntimeError as error:
                logging.debug("Caught a RuntimeError: %s", str(error))
                if validation.check_file(filename):
                    logging.debug('File [%s] already exists, ignore', filename)
                else:
                    raise Exception('Could not copy [%s] to [%s]' % (filename, tgt))


def move_stage_to_dropbox(stage, dropbox, keep_copy=False):
    """Move the stage box to its final name."""
    #empty when moved, stage_copy when keepcopy
    newstage = ""
    if keep_copy:
        newstage = stage + '_copy'
        shutil.copytree(stage, newstage)

    #extend permissions for dropbox copy job
    os.chmod(stage, 0o775)
    for dirpath, _, filenames in os.walk(stage):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            os.chmod(path, 0o775)

    logging.debug("Moving stage [%s] to dropbox [%s]", stage, dropbox)
    shutil.move(stage, dropbox)
    return newstage


def extend_workflow_id(wfstring):
    """Extends the workflow id. WARNING: used to be called extendWorkflowID."""
    applivers = subprocess.check_output(
        "git --git-dir=/cluster/apps/guse/stable/base/master/.git rev-parse --short HEAD"
        , shell=True).strip()
    imsbtoolvers = subprocess.check_output("printenv LOADEDMODULES | \
                                            grep -o 'imsbtools/[^:]*' | tail -1",
                                           shell=True).strip()
    return wfstring + " " + imsbtoolvers + " base@" + applivers
