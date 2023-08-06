# -*- coding: utf-8 -*-
"""
Package parameters:
-----------------------
 Flask-Mercury *query* parameter type definitions.
"""
import inspect
from ..base import BaseParameter
from flask import request


class BaseQueryParameter(BaseParameter):
    """
    Base path parameter class
    """
    _type = ""

    @classmethod
    def create(cls, name, value):
        pass

    @classmethod
    def to_swagger(cls, param, doc):
        """
        Base query parameter spec serialization function.
        """
        spec = super().to_swagger(param, doc)
        spec["in"] = "query"
        spec['type'] = cls._type

        return spec

    @classmethod
    def from_request(cls, name, meth, default=None):
        value = request.args.get(name, default)
        if value is not None:
            return cls.create(name, value)
        else:
            return None