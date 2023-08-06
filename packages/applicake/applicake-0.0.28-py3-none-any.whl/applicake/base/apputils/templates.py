"""Utils to support the use of templates."""
import inspect
from string import Template


def get_tpl_of_class(cls):
    """Find templates for a given class."""
    return inspect.getabsfile(cls.__class__).replace(".py", ".tpl")


def read_mod_write(info, infile, outfile):
    """Motify the template."""
    tpl = read_template(infile)
    mod_tpl = modify_template(info, tpl)
    write_template(mod_tpl, outfile)


def read_template(path):
    """Read the template."""
    tpl_fh = open(path, 'r')
    template = tpl_fh.read()
    return template


def modify_template(info, template):
    """
    replaces $VARS (or ${VARS}) in template IF found in info, otherwise leaves $VARS
    NOTE: The first non-identifier (![AZaz09_]) character after $ terminates varname
    """
    mod_template = Template(template).safe_substitute(info)
    return mod_template


def write_template(template, path):
    """Write the template."""
    tpl_fh = open(path, 'w')
    tpl_fh.write(template)
    tpl_fh.close()
