#!/usr/bin/python


class NodeTypeError(Exception):
    def __init__(self, message):
        super(NodeTypeError, self).__init__(message)


class NodeRegistrationError(Exception):
    def __init__(self, message):
        super(NodeRegistrationError, self).__init__(message)


class NodePluginError(Exception):
    def __init__(self, message):
        super(NodePluginError, self).__init__(message)


class NodePropertyError(Exception):
    def __init__(self, message):
        super(NodePropertyError, self).__init__(message)


class NodeMenuError(Exception):
    pass
