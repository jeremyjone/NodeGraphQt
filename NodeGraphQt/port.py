#!/usr/bin/python


class Port(object):

    def __init__(self, node=None, port=None):
        self.__node = node
        self.__item = port

    def __repr__(self):
        name = str(self.__class__.__name__)
        return '<{}(\'{}\') at {}>'.format(
            name, self.name(), hex(id(self))
        )

    def __str__(self):
        module = str(self.__class__.__module__)
        name = str(self.__class__.__name__)
        return module + '.' + name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.node().id() == other.node().id()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.type(), self.node().id()))

    @property
    def __port(self):
        """
        returns the PortItem() used in the scene.

        Returns:
            PortItem: port item.
        """
        return self.__item

    def name(self):
        """
        name of the port.

        Returns:
            str: port name.
        """
        return self.__port.name

    def node(self):
        """
        Return the parent node of the port.

        Returns:
            BlueprintNodeGraph.Node: node object.
        """
        return self.__node

    def type(self):
        """
        Returns the port type.

        Returns:
            str: 'in' = input port, 'out' = output port.
        """
        return self.__port.port_type

    def color(self):
        """
        Returns the default port color (red, green, blue).

        Returns:
            tuple: (r, g, b) from 0-255 range.
        """
        r, g, b, a = self.__port.color
        return r, g, b

    def set_color(self, r=0, g=0, b=0):
        """
        Sets the default port color in (red, green, blur, alpha) value.

        Args:
            r (int): red value 0-255 range.
            g (int): green value 0-255 range.
            b (int): blue value 0-255 range.
        """

        self.__port.color = (r, g, b, 255)

    def connected_pipes(self):
        """
        Return all connected pipes.

        Returns:
            list[NodeGraphQt.interfaces.Pipe]: list of pipe instances.
        """
        return [Pipe(p) for p in self.__port.connected_pipes]

    def connected_ports(self):
        """
        Returns all connected ports.

        Returns:
            list[NodeGraphQt.interfaces.Port]: list of connected ports.
        """
        return [Port(p.node, p) for p in self.__port.connected_ports]

    def connect_to(self, port=None):
        """
        Creates a pipe and connects it to the port with a connection.

        Args:
            port (NodeGraphQt.interfaces.Port): port object.
        """
        self.__port.connect_to(port.item)


class Pipe(object):

    def __init__(self, pipe=None):
        self.__item = pipe

    def __repr__(self):
        name = str(self.__class__.__name__)
        return '<{}(\'{}\') at {}>'.format(
            name, self.name(), hex(id(self))
        )

    def __str__(self):
        module = str(self.__class__.__module__)
        name = str(self.__class__.__name__)
        return module + '.' + name

    @property
    def __pipe(self):
        """
        returns the PipeItem() used in the scene.

        Returns:
            PortItem: pipe item.
        """
        return self.__item

    @property
    def input(self):
        """
        return the connected input port.

        Returns:
            NodeGraphQt.interfaces.Port: instance of the connected port.
        """
        port = self.__pipe.input_port
        return Port(port.node, port)

    @property
    def output(self):
        """
        return the connect output port.

        Returns:
            NodeGraphQt.interfaces.Port: instance of the connected port.
        """
        port = self.__pipe.output_port
        return Port(port.node, port)
