#!/usr/bin/python
from PySide2 import QtGui, QtCore, QtWidgets

from .constants import (IN_PORT, OUT_PORT,
                        PORT_HOVER_COLOR,
                        PORT_HOVER_BORDER_COLOR,
                        PORT_ACTIVE_COLOR,
                        PORT_ACTIVE_BORDER_COLOR,
                        Z_VAL_PORT)


class PortItem(QtWidgets.QGraphicsItem):
    """
    Base Port Item.
    """

    def __init__(self, parent=None, name=''):
        super(PortItem, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self.setFlag(self.ItemIsSelectable, False)
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setZValue(Z_VAL_PORT)
        self.__pipes = []
        self.__width = 10.0
        self.__height = 10.0
        self.__hovered = False
        self.__name = name
        self.__color = (49, 115, 100, 255)
        self.__border_color = (29, 202, 151, 255)
        self.__border_size = 1
        self.__port_type = None
        self.__multi_connection = False
        self.__display_name = True

    def __str__(self):
        return '{}.PortItem("{}")'.format(self.__module__, self.name)

    def __repr__(self):
        return '{}.PortItem("{}")'.format(self.__module__, self.name)

    def boundingRect(self):
        return QtCore.QRectF(0.0, 0.0, self.__width, self.__height)

    def paint(self, painter, option, widget):
        painter.save()

        rect = QtCore.QRectF(0.0, 0.8, self.__width, self.__height)
        painter.setBrush(QtGui.QColor(0, 0, 0, 200))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1.8))
        path = QtGui.QPainterPath()
        path.addEllipse(rect)
        painter.drawPath(path)

        if self.__hovered:
            color = QtGui.QColor(*PORT_HOVER_COLOR)
            border_color = QtGui.QColor(*PORT_HOVER_BORDER_COLOR)
        elif self.connected_pipes:
            color = QtGui.QColor(*PORT_ACTIVE_COLOR)
            border_color = QtGui.QColor(*PORT_ACTIVE_BORDER_COLOR)
        else:
            color = QtGui.QColor(*self.color)
            border_color = QtGui.QColor(*self.border_color)

        painter.setBrush(color)
        pen = QtGui.QPen(border_color, 1.5)
        painter.setPen(pen)
        painter.drawEllipse(self.boundingRect())

        painter.restore()

    def itemChange(self, change, value):
        if change == self.ItemScenePositionHasChanged:
            self.redraw_connected_pipes()
        return super(PortItem, self).itemChange(change, value)

    def mousePressEvent(self, event):
        if event.modifiers() != QtCore.Qt.AltModifier:
            self.viewer_start_connection()
        super(PortItem, self).mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        super(PortItem, self).mouseReleaseEvent(event)
        
    def hoverEnterEvent(self, event):
        self.__hovered = True
        super(PortItem, self).hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        self.__hovered = False
        super(PortItem, self).hoverLeaveEvent(event)

    def viewer_start_connection(self):
        viewer = self.scene().viewer()
        viewer.start_live_connection(self)

    def redraw_connected_pipes(self):
        if not self.connected_pipes:
            return
        for pipe in self.connected_pipes:
            if self.port_type == IN_PORT:
                pipe.draw_path(self, pipe.output_port)
            elif self.port_type == OUT_PORT:
                pipe.draw_path(pipe.input_port, self)

    def add_pipe(self, pipe):
        self.__pipes.append(pipe)

    def remove_pipe(self, pipe):
        self.__pipes.remove(pipe)

    @property
    def connected_pipes(self):
        return self.__pipes

    @property
    def connected_ports(self):
        ports = []
        port_types = {IN_PORT: 'output_port', OUT_PORT: 'input_port'}
        for pipe in self.connected_pipes:
            ports.append(getattr(pipe, port_types[self.port_type]))
        return ports

    @property
    def node(self):
        return self.parentItem()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name=''):
        self.__name = name.strip()

    @property
    def display_name(self):
        return self.__display_name

    @display_name.setter
    def display_name(self, display=True):
        self.__display_name = display

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color=(0, 0, 0, 255)):
        self.__color = color

    @property
    def border_color(self):
        return self.__border_color

    @border_color.setter
    def border_color(self, color=(0, 0, 0, 255)):
        self.__border_color = color

    @property
    def border_size(self):
        return self.__border_size

    @border_size.setter
    def border_size(self, size=2):
        self.__border_size = size

    @property
    def multi_connection(self):
        return self.__multi_connection

    @multi_connection.setter
    def multi_connection(self, mode=False):
        conn_type = 'multi' if mode else 'single'
        self.setToolTip('{}: ({})'.format(self.name, conn_type))
        self.__multi_connection = mode

    @property
    def port_type(self):
        return self.__port_type

    @port_type.setter
    def port_type(self, port_type):
        self.__port_type = port_type

    def delete(self):
        for pipe in self.connected_pipes:
            pipe.delete()
            # # TODO: not sure if we need this...
            # del pipe

    def connect_to(self, port):
        if not port:
            for pipe in self.connected_pipes:
                pipe.delete()
            return
        if self.scene():
            viewer = self.scene().viewer()
            viewer.connect_ports(self, port)
