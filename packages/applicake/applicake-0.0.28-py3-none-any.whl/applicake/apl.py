#!/usr/bin/env python3
"""
Executes main() function of class defined in argv[0]
Potentially unsafe but convenient.

Example usage:
alp.py examples.echobasic --COMMENT hello
"""
import importlib
import inspect
import sys
import re
import logging

LOGGER = logging.getLogger()
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)

def main():
    """main, find applicake app and execute main."""
    appliapp = None
    cls = None
    if len(sys.argv) <= 1 or not re.match(r"^[\w\.]+$", sys.argv[1]):
        print("Usage: %s NODE [OPTIONS]; e.g. %s examples.echobasic --COMMENT comment" %
              (sys.argv[0], sys.argv[0]))
        sys.exit(1)
    if '--WORKDIR' not in sys.argv:
        sys.argv.append('--WORKDIR')
        sys.argv.append('.')
    appliapp = 'appliapps.' + sys.argv[1]
    try:
        module = importlib.import_module(appliapp)
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and appliapp in obj.__module__:
                cls = obj
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError('Could not find/load app [%s]: %s' % (appliapp, str(error)))
    try:
        cls.main()
    except KeyError as error:
        raise KeyError('Missing key [%s]: %s' % (appliapp, str(error)))
    except Exception as error:
        raise Exception('General exception, could not run app [%s]: %s' % (appliapp, str(error)))


if __name__ == "__main__":
    main()
