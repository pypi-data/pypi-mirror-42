# -*- coding: utf-8 -*-
"""
Module utils.py
-----------------
 A set of utility functions that are used to build resources and swagger specification.
"""
import sys
from importlib import import_module
import six

def reindent(string):
    """
    | **function adapted from**
    |    https://github.com/openstack/rally/blob/7153e0cbc5b0e6433313a3bc6051b2c0775d3804/rally/common/plugin/info.py
    
    """
    return "\n".join(l.strip() for l in string.strip().split("\n"))


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    if '.' not in dotted_path:
        return import_module(dotted_path)
    else:

        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            msg = "%s doesn't look like a module path" % dotted_path
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError:
            msg = 'Module "{}" does not define a "{}" attribute/class'.format(
                dotted_path, class_name
            )
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


def is_integer(value):
    try:
        value = int(value)
        return True
    except:
        return False


def ensure_text_type(val):
    if isinstance(val, bytes):
        val = val.decode('utf-8')
    return str(val)