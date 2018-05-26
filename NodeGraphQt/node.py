#!/usr/bin/python
from NodeGraphQt import NodeBaseWidget
from .exceptions import NodeTypeError
from .model import NodeModel
from .port import Port
from .widgets.backdrop import BackdropNodeItem
from .widgets.base import BaseItem
from .widgets.node import NodeItem


class classproperty(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, instance, owner):
        return self.f(owner)


class NodeBase(object):
    """
    Base node object.
    """

    __identifier__ = 'nodeGraphQt.nodes'

    NODE_NAME = None

    def __init__(self):
        self._item = None
        self._model = None

    def __repr__(self):
        return '<{}(\'{}\') at {}>'.format(
            self.type.split('.')[-1], self.NODE_NAME, hex(id(self))
        )

    def __str__(self):
        return '{}(\'{}\')'.format(self.type(), self.NODE_NAME)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.type, self.id))

    def set_item(self, item=None):
        if not isinstance(item, BaseItem):
            raise NodeTypeError(
                '"{}" is not a instance of a node item.'.format(str(item))
            )
        self._item = item
        self._item.type = self.type
        self._item.name = self.NODE_NAME

    def set_model(self, model=None):
        self._model = model

    @property
    def _node(self):
        """
        QGraphicsItem used in the scene.

        Returns:
            QtWidgets.QGraphicsItem: node item.
        """
        return self._item

    @classproperty
    def type(cls):
        """
        node type identifier followed by the class name.
        eg. com.chantasticvfx.FooNode

        Returns:
            str: node type.
        """
        return cls.__identifier__ + '.' + cls.__name__

    @property
    def model(self):
        """
        The node model

        Returns:
            NodeModel: node model
        """
        return self._model

    @property
    def id(self):
        """
        The node unique id.

        Returns:
            str: unique id string.
        """
        return self._node.id

    def name(self):
        """
        Name of the node.

        Returns:
            str: name of the node.
        """
        return self._node.name

    def set_name(self, name=''):
        """
        Set the name of the node.

        Args:
            name (str): name for the node.
        """
        self._node.name = name
        self.NODE_NAME = self._node.name

    def color(self):
        """
        Returns the node color in (red, green, blue) value.

        Returns:
            tuple: (r, g, b) from 0-255 range.
        """
        r, g, b, a = self._node.color
        return r, g, b

    def set_color(self, r=0, g=0, b=0):
        """
        Sets the color of the node in (red, green, blue) value.

        Args:
            r (int): red value 0-255 range.
            g (int): green value 0-255 range.
            b (int): blue value 0-255 range.

        """
        self._node.color = (r, g, b, 255)

    def enable(self):
        """
        enables the node.
        """
        self._node.disabled = False

    def disable(self):
        """
        disables the node.
        """
        self._node.disabled = True

    def disabled(self):
        """
        returns weather the node is enabled or disabled.

        Returns:
            bool: true if the node is disabled.
        """
        return self._node.disabled

    def selected(self):
        """
        Returns the selected state of the node.

        Returns:
            bool: True if the node is selected.
        """
        return self._node.isSelected()

    def set_selected(self, selected=True):
        """
        Set the node to be selected or not selected.

        Args:
            selected (bool): True to select the node.
        """
        self._node.setSelected(selected)

    def properties(self):
        """
        Returns all the node properties.

        Returns:
            dict: a dictionary of node properties.
        """
        return self._node.properties

    def get_property(self, name):
        """
        Return the node property.

        Args:
            name (str): name of the property.

        Returns:
            str, int or float: value of the node property.
        """
        return self._model.get_property(name)

    def set_property(self, name, value):
        """
        Set the value on the node property.

        Args:
            name (str): name of the property.
            value: the new property value.
        """
        if name in self._node.item_properties.keys():
            self._node.set_item_property(name, value)
        self._model.set_property(name, value)

    def set_x_pos(self, x=0.0):
        """
        Set the node horizontal X position in the node graph.

        Args:
            x (float): node x position:
        """
        y = self._node.pos().y()
        self.set_pos(x, y)

    def set_y_pos(self, y=0.0):
        """
        Set the node horizontal Y position in the node graph.

        Args:
            y (float): node x position:
        """
        x = self._node.pos().x()
        self.set_pos(x, y)

    def set_pos(self, x=0.0, y=0.0):
        """
        Set the node X and Y position in the node graph.
        Args:
            x (float): node X position.
            y (float): node Y position.
        """
        self._node.pos = [x, y]

    def x_pos(self):
        """
        Get the node X position in the node graph.

        Returns:
            float: x position.
        """
        return self._node.pos[0]

    def y_pos(self):
        """
        Get the node Y position in the node graph.

        Returns:
            float: y position.
        """
        return self._node.pos[1]

    def pos(self):
        """
        Get the node XY position in the node graph.

        Returns:
            tuple(float, float): x and y position.
        """
        return self._node.pos


class Node(NodeBase):
    """
    Base class of a Node object.
    """

    NODE_NAME = 'Base node'

    def __init__(self):
        super(Node, self).__init__()
        self.set_item(NodeItem())
        self.set_model(NodeModel(self))

    def set_icon(self, icon=None):
        """
        Set the node icon.

        Args:
            icon (str): path to the icon image. 
        """
        self._node.icon = icon

    def add_input(self, name='input', multi_input=False, display_name=True):
        """
        Adds a input port the the node.

        Args:
            name (str): name for the input port. 
            multi_input (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
            
        Returns:
            NodeGraphQt.interfaces.Port: the created port object.
        """
        port_item = self._node.add_input(name, multi_input, display_name)
        return Port(self, port=port_item)

    def add_output(self, name='output', multi_output=True, display_name=True):
        """
        Adds a output port the the node.

        Args:
            name (str): name for the output port. 
            multi_output (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
             
        Returns:
            NodeGraphQt.interfaces.Port: the created port object.
        """
        port_item = self._node.add_output(name, multi_output, display_name)
        return Port(self, port=port_item)

    def add_combo_menu(self, name='', label='', items=None):
        """
        Embed a NodeComboBox widget into the node.

        Args:
            name (str): name of the widget.
            label (str): label to be displayed.
            items (list[str]): items to be added into the menu.
        """
        self._node.add_combo_menu(name, label, items)

    def add_text_input(self, name='', label='', text=''):
        """
        Embed a NodeLineEdit widget into the node.

        Args:
            name (str): name of the widget.
            label (str): label to be displayed.
            text (str): pre filled text.
        """
        self._node.add_text_input(name, label, text)

    def add_checkbox(self, name='', label='', text='', state=False):
        """
        Embed a NodeCheckBox widget into the node.

        Args:
            name (str): name of the widget.
            label (str): label to be displayed.
            text (str): QCheckBox text.
            state (bool): pre-check.
        """
        self._node.add_checkbox(name, label, text, state)

    def add_widget(self, widget):
        """
        Embed a custom widget into the node.

        Args:
            widget (NodeGraphQt.NodeBaseWidget): node widget.
        """
        name = widget.name
        if not isinstance(widget, NodeBaseWidget):
            raise TypeError('Object must be a instance of a NodeBaseWidget')
        if name in self._node.widgets.keys():
            raise KeyError('widget name "{}" already exists'.format(name))
        self._node.add_widget(widget)

    def get_widget(self, name):
        """
        returns the node widget from the name.

        Args:
            name (str): name of the widget.

        Returns:
            NodeWidget: node widget.
        """
        if not self._node.widgets.get(name):
            raise KeyError('node has no widget "{}"'.format(name))
        return self._node.widgets.get(name)

    def all_widgets(self):
        """
        return all node widgets.

        Returns:
            dict: {widget_name : node_widget}
        """
        return self._node.widgets

    def inputs(self):
        """
        Returns all the input port for the node.
        
        Returns:
            dict: {port name: port object}
        """
        return {p.name: Port(self, p) for p in self._node.inputs}

    def outputs(self):
        """
        Returns all the output port for the node.

        Returns:
            dict: {port name: port object}
        """
        return {p.name: Port(self, p) for p in self._node.outputs}

    def input(self, index):
        """
        Return the input port with the matching index.

        Args:
            index (int): index of the input port.

        Returns:
            NodeGraphQt.interfaces.Port: port object.
        """
        return Port(self, port=self._node.inputs[index])

    def set_input(self, index, port):
        """
        Creates a connection pipe to the targeted output port.

        Args:
            index (int): index of the port.
            port (NodeGraphQt.interfaces.Port): port object.
        """
        src_port = Port(self, port=self._node.inputs[index])
        src_port.connect_to(port)

    def output(self, index):
        """
        Return the output port with the matching index.

        Args:
            index (int): index of the output port.

        Returns:
            NodeGraphQt.interfaces.Port: port object.
        """
        return Port(self, port=self._node.outputs[index])

    def set_output(self, index, port):
        """
        Creates a connection pipe to the targeted input port.

        Args:
            index (int): index of the port.
            port (NodeGraphQt.interfaces.Port): port object.
        """
        src_port = Port(self, port=self._node.outputs[index])
        src_port.connect_to(port)


class BackdropNode(NodeBase):
    """
    Base class of a Backdrop node.
    """

    NODE_NAME = 'Backdrop'

    def __init__(self):
        super(BackdropNode, self).__init__()
        self.set_item(BackdropNodeItem())
        self.set_model(NodeModel(self))

    def set_text(self, text):
        """
        Sets the text to be displayed in the backdrop node.

        Args:
            text (str): text string.
        """
        self._node.text = text

    def text(self):
        """
        returns the text on the backdrop node.

        Returns:
            str: text string.
        """
        return self._node.text

    def width(self):
        """
        Returns the width of the backdrop.

        Returns:
            float: backdrop width.
        """
        return self._node.width

    def set_width(self, width):
        """
        Sets the backdrop width.

        Args:
            width (float): width size.
        """
        self._node.width = width

    def height(self):
        """
        Returns the height of the backdrop.

        Returns:
            float: backdrop height.
        """
        return self._node.height

    def set_height(self, height):
        """
        Sets the backdrop height.

        Args:
            height (float): width size.
        """
        self._node.height = height
