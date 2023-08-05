# coding: utf-8

"""
    Marquez

    Marquez is an open source **metadata service** for the **collection**, **aggregation**, and **visualization** of a data ecosystem's metadata.  # noqa: E501

    OpenAPI spec version: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class CreateNamespace(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'owner': 'str',
        'description': 'str'
    }

    attribute_map = {
        'owner': 'owner',
        'description': 'description'
    }

    def __init__(self, owner=None, description=None):  # noqa: E501
        """CreateNamespace - a model defined in OpenAPI"""  # noqa: E501

        self._owner = None
        self._description = None
        self.discriminator = None

        self.owner = owner
        if description is not None:
            self.description = description

    @property
    def owner(self):
        """Gets the owner of this CreateNamespace.  # noqa: E501

        The owner of the namespace.  # noqa: E501

        :return: The owner of this CreateNamespace.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this CreateNamespace.

        The owner of the namespace.  # noqa: E501

        :param owner: The owner of this CreateNamespace.  # noqa: E501
        :type: str
        """
        if owner is None:
            raise ValueError("Invalid value for `owner`, must not be `None`")  # noqa: E501

        self._owner = owner

    @property
    def description(self):
        """Gets the description of this CreateNamespace.  # noqa: E501

        The description of the namespace.  # noqa: E501

        :return: The description of this CreateNamespace.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateNamespace.

        The description of the namespace.  # noqa: E501

        :param description: The description of this CreateNamespace.  # noqa: E501
        :type: str
        """

        self._description = description

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateNamespace):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
