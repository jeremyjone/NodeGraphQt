#!/usr/bin/python
from PySide2 import QtCore, QtWidgets

from .constants import Z_VAL_NODE, NODE_COLOR, NODE_BORDER_COLOR, NODE_TEXT_COLOR
from NodeGraphQt.exceptions import NodePropertyError


class BaseItem(QtWidgets.QGraphicsItem):
    """
    The abstract base class of a node.
    """

    def __init__(self, name='node', parent=None):
        super(BaseItem, self).__init__(parent)
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setZValue(Z_VAL_NODE)
        self._prev_pos = self.pos
        self._width = 120
        self._height = 80
        self._properties = {
            'id': hex(id(self)),
            'name': name,
            'color': NODE_COLOR,
            'border_color': NODE_BORDER_COLOR,
            'text_color': NODE_TEXT_COLOR,
            'type': None,
            'selected': False,
            'disabled': False,
        }

    def __str__(self):
        return '{}(\'{}\')'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        module = self.__module__
        class_name = self.__class__.__name__
        return '{}.{}(\'{}\')'.format(module, class_name, self.name)

    def boundingRect(self):
        return QtCore.QRectF(0.0, 0.0, self._width, self._height)

    def mousePressEvent(self, event):
        self._properties['selected'] = True
        super(BaseItem, self).mousePressEvent(event)

    def setSelected(self, selected):
        self._properties['selected'] = selected
        super(BaseItem, self).setSelected(selected)

    def setPos(self, *args, **kwargs):
        super(BaseItem, self).setPos(*args, **kwargs)
        self._properties['pos'] = (float(self.scenePos().x()),
                                   float(self.scenePos().y()))

    def viewer(self):
        """
        return the main viewer.

        Returns:
            NodeGraphQt.widgets.viewer.NodeViewer: viewer object.
        """
        if self.scene():
            return self.scene().viewer()

    def pre_init(self, viewer, pos=None):
        """
        Called before node item has been added into the scene.

        Args:
            viewer (NodeGraphQt.widgets.viewer.NodeViewer): main viewer.
            pos (tuple): the cursor pos if node is called with tab search.
        """
        pass

    def post_init(self, viewer, pos=None):
        """
        Called after node item has been added into the scene.

        Args:
            viewer (NodeGraphQt.widgets.viewer.NodeViewer): main viewer
            pos (tuple): the cursor pos if node is called with tab search.
        """
        pass

    def set_item_property(self, name, value):
        """
        Set the attributes on the item.

        Args:
            name (str): name of the item property.
            value (): value for the property.
        """
        if self._properties.get(name):
            if isinstance(value, type(value)):
                setattr(self, name, value)
            else:
                raise NodePropertyError(
                    'item property "{}" value must be a {}'
                    .format(name, type(self.properties[name]).title())
                )
        else:
            raise NodePropertyError(
                'item "{}" has no property "{}"'.format(self.name, name)
            )

    @property
    def item_properties(self):
        """
        return all node item properties.

        Returns:
            dict: {property_name: property_value}
        """
        return self._properties

    @property
    def id(self):
        return self._properties['id']

    @id.setter
    def id(self, unique_id=''):
        self._properties['id'] = unique_id

    @property
    def type(self):
        return self._properties['type']

    @type.setter
    def type(self, node_type='NODE'):
        self._properties['type'] = node_type

    @property
    def size(self):
        return self._width, self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width=0.0):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height=0.0):
        self._height = height

    @property
    def color(self):
        return self._properties['color']

    @color.setter
    def color(self, color=(0, 0, 0, 255)):
        self._properties['color'] = color

    @property
    def text_color(self):
        return self._properties['text_color']

    @text_color.setter
    def text_color(self, color=(100, 100, 100, 255)):
        self._properties['text_color'] = color

    @property
    def border_color(self):
        return self._properties['border_color']

    @border_color.setter
    def border_color(self, color=(0, 0, 0, 255)):
        self._properties['border_color'] = color

    @property
    def disabled(self):
        return self._properties['disabled']

    @disabled.setter
    def disabled(self, state=False):
        self._properties['disabled'] = state

    @property
    def selected(self):
        return self.isSelected()

    @selected.setter
    def selected(self, selected=False):
        self.setSelected(selected)

    @property
    def pos(self):
        return float(self.scenePos().x()), float(self.scenePos().y())

    @pos.setter
    def pos(self, pos=None):
        if pos:
            self.setPos(pos[0], pos[1])

    @property
    def name(self):
        return self._properties['name']

    @name.setter
    def name(self, name=''):
        viewer = self.viewer()
        if viewer:
            name = viewer.get_unique_node_name(name)
        self._properties['name'] = name
        self.setToolTip('node: {}'.format(name))

    def delete(self):
        """
        delete node item from the scene.
        """
        if self.scene():
            self.scene().removeItem(self)

    def to_dict(self):
        """
        serialize node object to a dict:.

        Returns:
            dict: node id as the key and properties as the values eg.
                {'0x106cf75a8': {
                    'name': 'foo node',
                    'color': (48, 58, 69, 255),
                    'border_color': (85, 100, 100, 255),
                    'text_color': (255, 255, 255, 180),
                    'type': 'com.chantasticvfx.FooNode',
                    'selected': False,
                    'disabled': False,
                    'pos': (0.0, 0.0)
                    }
                }
        """
        serial = {
            self.id: {k: v for k, v in self._properties.items() if k != 'id'}
        }
        return serial

    def from_dict(self, node_dict):
        """
        deserialize dict to node.

        Args:
            node_dict (dict): serialized node dict.
        """
        for name, value in node_dict.items():
            if hasattr(self, name):
                setattr(self, name, value)
            else:
                self._properties[name] = value
