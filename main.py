import sys

from PySide2 import QtWidgets

from widgets.game import PlaySpace

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    space = PlaySpace()
    space.show()
    sys.exit(app.exec_())
