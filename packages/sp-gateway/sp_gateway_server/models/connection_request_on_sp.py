# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from sp_gateway_server.models.base_model_ import Model
from sp_gateway_server import util


class ConnectionRequestOnSP(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, me_host=None, scheme=None):  # noqa: E501
        """ConnectionRequestOnSP - a model defined in OpenAPI

        :param me_host: The me_host of this ConnectionRequestOnSP.  # noqa: E501
        :type me_host: str
        :param scheme: The scheme of this ConnectionRequestOnSP.  # noqa: E501
        :type scheme: str
        """
        self.openapi_types = {
            'me_host': str,
            'scheme': str
        }

        self.attribute_map = {
            'me_host': 'me_host',
            'scheme': 'scheme'
        }

        self._me_host = me_host
        self._scheme = scheme

    @classmethod
    def from_dict(cls, dikt) -> 'ConnectionRequestOnSP':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ConnectionRequestOnSP of this ConnectionRequestOnSP.  # noqa: E501
        :rtype: ConnectionRequestOnSP
        """
        return util.deserialize_model(dikt, cls)

    @property
    def me_host(self):
        """Gets the me_host of this ConnectionRequestOnSP.


        :return: The me_host of this ConnectionRequestOnSP.
        :rtype: str
        """
        return self._me_host

    @me_host.setter
    def me_host(self, me_host):
        """Sets the me_host of this ConnectionRequestOnSP.


        :param me_host: The me_host of this ConnectionRequestOnSP.
        :type me_host: str
        """

        self._me_host = me_host

    @property
    def scheme(self):
        """Gets the scheme of this ConnectionRequestOnSP.


        :return: The scheme of this ConnectionRequestOnSP.
        :rtype: str
        """
        return self._scheme

    @scheme.setter
    def scheme(self, scheme):
        """Sets the scheme of this ConnectionRequestOnSP.


        :param scheme: The scheme of this ConnectionRequestOnSP.
        :type scheme: str
        """

        self._scheme = scheme
