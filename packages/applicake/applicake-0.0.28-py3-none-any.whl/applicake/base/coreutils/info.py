"""Core utility, info handlers."""
from configobj import ConfigObj

from applicake.base.coreutils import Keys


def get_handler(path):
    """This is the factory method."""
    if path is None or path == '':
        return NoneInfoHandler()
    if ".ini" in path:
        return IniInfoHandler()
    raise Exception("Unknown info type " + path)


class IInfoHandler:
    """Base info handler."""
    def read(self, path):
        """Read the file, not implemented."""
        raise NotImplementedError

    def write(self, info, path):
        """Write the file, not implemented."""
        raise NotImplementedError

    def write_all(self, info, path):
        """Write the file without filters, not implemented."""
        raise NotImplementedError


class NoneInfoHandler(IInfoHandler):
    """None Info Handler."""

    def read(self, path):
        """Read the file."""
        return {}

    def write(self, info, path):
        """Write the file."""

    def write_all(self, info, path):
        """Write the file, without filters."""


class IniInfoHandler(IInfoHandler):
    """Ini info handler."""

    def read(self, path):
        """Read the file."""
        return ConfigObj(path)

    def write(self, info, path):
        """Write the file."""
        info = info.copy()
        for key in [Keys.INPUT, Keys.OUTPUT, Keys.NAME, Keys.WORKDIR,
                    Keys.EXECUTABLE, Keys.ALL_ARGS]:
            if key in info:
                del info[key]
        config = ConfigObj(info)
        config.filename = path
        config.write()

    def write_all(self, info, path):
        """ same as write but does not do special key filtering. For debug purposes only."""
        info = info.copy()
        config = ConfigObj(info)
        config.filename = path
        config.write()
