# -*- coding: utf-8 -*-
"""
Package parameters:
-----------------------
 Flask-Mercury integer query parameter type.
"""
from .base import BaseQueryParameter
from werkzeug.exceptions import BadRequest
from ...properties import IntegerProperty
import inspect


class Integer(BaseQueryParameter, IntegerProperty):
    """
    Integer query parameter type.
    """
    _type = 'integer'

    @classmethod
    def create(cls, name, value):
        """
        Integer query parameter constructor.
        :param value: a value to be casted to int.
        :return: the value casted to int type
        """
        try:
            value = int(value)
            return value
        except ValueError as e:
            raise BadRequest(
                "Wrong type for the query parameter named '{}'. "
                "It should be an integer but we got '{}'.".format(name, value)
            )

    @classmethod
    def to_swagger(cls, param, doc):
        """
        Swagger spec query parameter serialization function.
        :param param: function parameter pointer.
        :param doc: the parameter doc_string.
        :return: the parameter spec.
        """
        spec = super().to_swagger(param, doc)
        spec['type'] = cls._type

        return spec

    @classmethod
    def __instancecheck__(cls, instance):
        """
        The magic function called to implement isinstance(..) functionality.
        :param instance: the object being evaluated.
        :return: true if instance should be considered a (direct or indirect) instance of class.
        """
        # builtin int type should be considered a instance of the Integer cls.
        if isinstance(instance, int):
            return True

        if type(instance) is cls:
            return True

        # TODO add parameter name to the message
        raise BadRequest(
            "Wrong type for the query parameter. "
            "It should be an integer but we got '{}'.".format(instance)
        )