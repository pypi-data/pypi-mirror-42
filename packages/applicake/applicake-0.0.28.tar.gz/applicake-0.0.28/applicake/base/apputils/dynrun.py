"""dynrun - the dynamic runner."""
import sys
import importlib
import inspect

def run(appliapp, inp, outp, workdir, extra_argv):
    """dynrun, dynamic runner."""
    cls = None
    sys.argv = ['--INPUT', inp, '--OUTPUT', outp, '--WORKDIR', workdir]
    sys.argv.extend(extra_argv)
    appliapp = 'appliapps.' + appliapp
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
