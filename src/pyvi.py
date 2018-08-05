#!/usr/bin/env python3
import sys
from PySide2 import QtWidgets
from pyvi.controller import PyviController
from pyvi.gui import *

def main():
    app = QtWidgets.QApplication(sys.argv)
    pyvi = PyviController()

    main_window = Pyvi_main_window(pyvi)
    main_window.show()

    pyvi.start()


    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
