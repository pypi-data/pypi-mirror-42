"""validation: various methods to check if the execution was successful."""
import os
import logging
from xml.parsers import expat


def check_exitcode(exit_code):
    """Check the exit code."""
    if exit_code == 0:
        logging.debug("Exit code OK (0)")
    else:
        raise RuntimeError("Bad exit code (%d)" % exit_code)


def check_stdout(stdout):
    """Check the stdout."""
    for line in stdout.splitlines():
        if any(x in line for x in ["Disk quota exceeded"]):
            raise RuntimeError("%s. Job ran out of scratch space! \
                                Please remove old workflow files!" % line.strip())
        if any(x in line for x in ["std::bad_alloc", "MemoryError"]):
            raise RuntimeError("%s. The job run out of RAM!" % line.strip())
        if any(x in line for x in ["Exception:", "IOError"]):
            raise RuntimeError("%s. Check stdout for more details!" % line.strip())
    logging.debug("No known error message in stdout")


def check_file(path):
    """Check if a file exists."""
    if not os.path.exists(path):
        raise RuntimeError('path [%s] does not exist' % path)
    if not os.path.isfile(path):
        raise RuntimeError('path [%s] is no file' % path)
    if not os.access(path, os.R_OK):
        raise RuntimeError('file [%s] cannot be read' % path)
    if not os.path.getsize(path) > 0:
        raise RuntimeError('file [%s] is 0KB' % path)
    else:
        logging.debug('file [%s] checked successfully', path)


def check_xml(path):
    """Check xml files."""
    check_file(path)
    try:
        parser = expat.ParserCreate()
        parser.ParseFile(open(path, "r"))
    except RuntimeError as error:
        raise RuntimeError("Invalid XML [%s]: %s" % (path, str(error)))
