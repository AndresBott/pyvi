#!/usr/bin/env python3
import sys
import os
from PySide2 import QtGui, QtCore, QtWidgets
from pyvi.controller import PyviController


class Pyvi_main_window(QtWidgets.QMainWindow):
    def __init__(self,pyvi_ctrl):

        super(Pyvi_main_window, self).__init__()

        # desktop = QtWidgets.QApplication.desktop()
        # resolution = desktop.availableGeometry()
        #
        # self.setMinimumWidth(resolution.width() / 7)
        # self.setMinimumHeight(resolution.height() / 8)

        # TODO add initial size config
        self.main_widget = Pyvi_CentralWidget(self,pyvi_ctrl)
        self.setCentralWidget(self.main_widget)

        # keyboard shortcuts are window bound
        self.keyReleaseEvent = pyvi_ctrl.on_main_window_key_release
        self.keyPressEvent = pyvi_ctrl.on_main_window_key_press
        pyvi_ctrl.main_window = self

    def center(self):
        # TODO make the center screen aware
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Pyvi_CentralWidget(QtWidgets.QWidget):

    def __init__(self, parent=None,pyvi_ctrl=None):
        super().__init__(parent)

        # print("w:" + str(self.width()) + " h:" + str(self.height()) )

        self.videoframe = Pyvi_video_frame(self,pyvi_ctrl)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxlayout)

        pyvi_ctrl.central_widget = self


        # overlay = Overlay(self)


class Pyvi_video_frame(QtWidgets.QFrame):
    def __init__(self, parent=None,pyvi_ctrl=None):
        super().__init__(parent)

        self.palette = self.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(44, 44, 44))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

        self.mouseDoubleClickEvent = pyvi_ctrl.on_video_double_click
        self.mouseReleaseEvent = pyvi_ctrl.on_video_click_release
        self.mousePressEvent = pyvi_ctrl.on_video_click_press

        pyvi_ctrl.on_video_frame_load(self.winId())



class Pyvi_overlay(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):

        QtWidgets.QGraphicsView.__init__(self, parent=parent)


        self.button = QPushButton("Bt")

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.button)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxlayout)

    def display_image(self):
        self.scene.clear()
        # w, h = img.size
        self.imgQ = QtGui.QImage('folder-html.png')  # we need to hold reference to imgQ, or it will crash
        pixMap = QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
        # self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        self.scene.update()
