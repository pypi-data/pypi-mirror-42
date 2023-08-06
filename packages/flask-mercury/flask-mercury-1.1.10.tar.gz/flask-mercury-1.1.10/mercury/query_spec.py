# -*- coding: utf-8 -*-
"""
Module query_spec.py
---------------------
    Defines a base query parameter group specification class.
"""
from simple_mappers import MapDefinition
from . import parameters
import inspect
from flask import request
import json
from werkzeug import exceptions as http_exceptions


class QuerySpec(MapDefinition):
    """Base Query Parameters group spec class.
    QuerySpec defines a group of query parameters for the resource request.
    """
    def __init__(self, map_undefined=False, **kwargs):
        super().__init__(map_undefined, **kwargs)

    @classmethod
    def to_swagger(cls, param, doc):
        """
        A Model class to swagger schema serialization.
        :param spec: A dict object used to store and represent the swagger specification.
        """
        specs = []
        for param_name, param_def in cls.__properties__.items():
            spec = cls.param_to_swagger(param_def)
            specs.append(spec)
        return specs

    @classmethod
    def param_to_swagger(cls, param: parameters.query.BaseQueryParameter):
        """
        Parameter to swagger schema serialization.
        :param param: parameter definition.
        """
        parameters.query.Boolean()
        spec = {
            "name": param.mapping_from or param.property_name,
        }
        if param.description is not None:
            spec["description"] = param.description

        if param.default is not inspect._empty:
            spec["required"] = False
        else:
            spec["required"] = True

        spec["in"] = "query"
        spec["type"] = param._type
        return spec

    @classmethod
    def from_request(cls, name, meth, default=None):
        args = request.args.to_dict()
        return cls.from_dict(args)
