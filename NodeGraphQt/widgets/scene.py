#!/usr/bin/python
from PySide2 import QtGui, QtCore, QtWidgets

from .constants import VIEWER_BG_COLOR, VIEWER_GRID_OVERLAY, VIEWER_GRID_COLOR
from .viewer import NodeViewer


class NodeScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent=None):
        super(NodeScene, self).__init__(parent)
        self.background_color = VIEWER_BG_COLOR
        self.grid = VIEWER_GRID_OVERLAY
        self.grid_color = VIEWER_GRID_COLOR

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return '{}.{}()'.format(self.__module__, self.__class__.__name__)

    def mousePressEvent(self, event):
        selected_nodes = self.viewer().selected_nodes()
        if self.viewer():
            self.viewer().sceneMousePressEvent(event)
        super(NodeScene, self).mousePressEvent(event)
        keep_selection = any([
            event.button() == QtCore.Qt.MiddleButton,
            event.button() == QtCore.Qt.RightButton,
            event.modifiers() == QtCore.Qt.AltModifier
        ])
        if keep_selection:
            for node in selected_nodes:
                node.setSelected(True)

    def mouseMoveEvent(self, event):
        if self.viewer():
            self.viewer().sceneMouseMoveEvent(event)
        super(NodeScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.viewer():
            self.viewer().sceneMouseReleaseEvent(event)
        super(NodeScene, self).mouseReleaseEvent(event)

    def drawBackground(self, painter, rect):
        painter.save()
        color = QtGui.QColor(*self.__bg_color)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
        painter.setBrush(color)
        painter.drawRect(rect.normalized())
        if not self.__grid:
            return
        grid_size = 20
        zoom = self.viewer().get_zoom()
        color = QtGui.QColor(*self.grid_color)
        if zoom > -4:
            pen = QtGui.QPen(color, 0.65)
            self.__draw_grid(painter, rect, pen, grid_size)

        color = color.darker(150)
        pen = QtGui.QPen(color, 0.65)
        self.__draw_grid(painter, rect, pen, grid_size * 8)
        painter.restore()

    def __draw_grid(self, painter, rect, pen, grid_size):
        lines = []
        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)
        x = left
        while x < rect.right():
            x += grid_size
            lines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
        y = top
        while y < rect.bottom():
            y += grid_size
            lines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
        painter.setPen(pen)
        painter.drawLines(lines)

    def viewer(self):
        if self.views() and isinstance(self.views()[0], NodeViewer):
            return self.views()[0]

    @property
    def grid(self):
        return self.__grid

    @grid.setter
    def grid(self, mode=True):
        self.__grid = mode

    @property
    def grid_color(self):
        return self.__grid_color

    @grid_color.setter
    def grid_color(self, color=(0, 0, 0)):
        self.__grid_color = color

    @property
    def background_color(self):
        return self.__bg_color

    @background_color.setter
    def background_color(self, color=(0, 0, 0)):
        self.__bg_color = color
