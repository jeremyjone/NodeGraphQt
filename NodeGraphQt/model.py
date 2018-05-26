#!/usr/bin/python
from .exceptions import NodePropertyError


class NodeModel(object):

    def __init__(self, node):
        node_item = node._node()
        for node_id, node_props in node_item.items():
            self._id = node_id
            self._properties = node_props

    @property
    def properties(self):
        return self._properties

    def add_property(self, name, default_value):
        if name in self._properties.keys():
            raise NodePropertyError('property {} already exists!'.format(name))
        self._properties[name] = default_value

    def set_property(self, name, value):
        if self._properties.get(name):
            self._properties[name] = value
        else:
            raise NodePropertyError(
                'no property "{}" in NodeModel'.format(name)
            )

    def get_property(self, name):
        return self._properties.get(name)

    def to_dict(self):
        serial = {
            self._id: {k: v for k, v in self._properties.items() if k != 'id'}
        }
        return serial
