import sys

from widgets.game import PlaySpace

from PySide2 import QtWidgets


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PlaySpace()
    window.show()
    sys.exit(app.exec_())
