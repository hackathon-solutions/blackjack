from PySide2 import QtWidgets, QtGui, QtCore

from config import config, APP_TITLE, ICON, PLACE_BACKGROUND
from widgets import helpers


class PlaySpace(QtWidgets.QWidget):
    def __init__(self, w: int = 900, h: int = 600):
        super().__init__()
        self._w = w
        self._h = h
        self.setWindowTitle(config(APP_TITLE))
        self.setWindowIcon(QtGui.QIcon(config(ICON)))
        self.setMinimumSize(self._w, self._h)
        self.setMaximumSize(self._w, self._h)

    def paintEvent(self, arg__1):
        pixmap = QtGui.QPixmap(config(PLACE_BACKGROUND)).scaled(self._w, self._h, QtCore.Qt.KeepAspectRatio)
        QtGui.QPainter(self).drawPixmap(0, 0, pixmap)


class CardFrame(QtWidgets.QFrame):
    def __init__(self, card_id: str, w: int = 64, h: int = 86):
        super().__init__()
        self._cover = helpers.CardImageLoader(card_id).get_image()
        self._w = w
        self._h = h

    def paintEvent(self, arg__1):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap.fromImage(self._cover).scaled(self._w, self._h, QtCore.Qt.KeepAspectRatio)
        painter.drawPixmap(0, 0, pixmap)
