# -*- coding: utf-8 -*-
"""
Package parameters:
-----------------------
 Flask-Mercury base parameter type definition.
"""
import inspect
from simple_mappers.properties.properties import BaseProperty

class MetaParameter(type):
    """
    Mercury Parameter metaclass.
    """
    def __instancecheck__(cls, instance):
        """
        The magic function called to implement isinstance(..) functionality.
        :param instance: the object being evaluated.
        :return: true if instance should be considered a (direct or indirect) instance of class.
        """
        return cls.__instancecheck__(instance)


class BaseParameter(BaseProperty, metaclass=MetaParameter):
    """
    Base Mercury parameter class.
    """
    flask_type = ""

    def __init__(self, description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description

    @classmethod
    def to_swagger(cls, param, doc):
        """
        Base function parameter spec serialization function.
        """
        spec = {
            "name": param.name,
        }
        if doc is not None:
            spec["description"] = doc

        if param.default is not inspect._empty:
            spec["required"] = False
        else:
            spec["required"] = True

        return spec

    @classmethod
    def __instancecheck__(cls, instance):
        """
        The magic function called to implement isinstance(..) functionality.
        :param instance: the object being evaluated.
        :return: true if instance should be considered a (direct or indirect) instance of class.
        """
        pass

