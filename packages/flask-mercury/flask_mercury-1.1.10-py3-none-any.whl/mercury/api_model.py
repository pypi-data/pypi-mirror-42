# -*- coding: utf-8 -*-
"""
Module api_model.py 
---------------------
    Defines the base class to the resource body.
"""
from simple_mappers import MapDefinition
import inspect
from flask import request
import json
from werkzeug import exceptions as http_exceptions


class ApiModel(MapDefinition):
    """An base ApiModel.
    ApiModel defines the structure of the resources body message.
    """
    def __init__(self, map_undefined=False, **kwargs):
        super().__init__(map_undefined, **kwargs)

    @classmethod
    def to_swagger(cls, spec):
        """
        A Model class to swagger schema serialization.
        :param spec: A dict object used to store and represent the swagger specification.
        """
        model_schema = dict()

        model_schema["type"] = "object"
        model_schema["properties"] = dict()
        for property_name, property_def in cls.__properties__.items():
            p_name = property_def.mapping_from or property_name

            model_schema["properties"][p_name] = property_def.to_swagger(dict())
        spec.definitions[cls.__name__] = model_schema
        return spec

    @classmethod
    def to_swagger_as_parameter(cls, param, doc):
        """
        Serializes a api model as a resource verb parameter.
        :param param: a verb implementation parameter.
        :param doc: a parameter doc string.
        :return: the swagger parameter specification.
        """
        # parameter spec
        pspec = dict()
        pspec['name'] = param.name
        pspec['description'] = doc
        if param.default is inspect._empty:
            pspec["required"] = True
        else:
            pspec["required"] = False

        pspec["in"] = "body"
        pspec["schema"] = {"$ref": "#/definitions/{}".format(cls.__name__)}
        return pspec

    @classmethod
    def to_swagger_as_form(cls):
        """
        Serializes a api model as a set of form's parameter.
        :param param: a verb implementation parameter.
        :param doc: a parameter doc string.
        :return: the swagger parameter specification.
        """
        parameters_set = list()
        for property_name, property_def in cls.__properties__.items():
            pspec = dict()
            p_name = property_name if property_def.mapping_from is None else property_def.mapping_from
            pspec['name'] = p_name
            pspec = property_def.to_swagger(pspec)
            pspec["in"] = "formData"
            parameters_set.append(pspec)

        return parameters_set

    @classmethod
    def to_swagger_as_response(cls, doc):
        spec = {
            "schema": {
                "$ref": "#/definitions/{}".format(cls.__name__)
            }
        }
        if doc is not None:
            spec["description"] = doc
        return spec

    @classmethod
    def from_request(cls, name, meth, default=None):
        if "multipart/form-data" in meth.__pdoc__.consumes:
            data = dict()
            data.update({key: value for key, value in request.form.items()})
            data.update({key: value for key, value in request.files.items()})

            try:
                if len(data) > 0:
                    return cls.from_dict(data)
                else:
                    return default
            except Exception as e:
                raise http_exceptions.BadRequest(str(e))

        else:
            if request.data is not None:
                # decode the request data body
                data = request.data.decode("utf-8").strip()
                try:
                    if data != "":
                        data = json.loads(data)
                        return cls.from_dict(data)
                    else:
                        return default
                except Exception as e:
                    raise http_exceptions.BadRequest(str(e))
