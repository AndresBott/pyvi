#!/usr/bin/env python

import sys
import os
from vlc import vlc

from ctypes import pythonapi, c_void_p, py_object

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PIL import Image,  ImageEnhance


import time

try:
    unicode        # Python 2
except NameError:
    unicode = str  # Python 3

class Player_Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Player_Main_Window, self).__init__()

        # desktop = QtWidgets.QApplication.desktop()
        # resolution = desktop.availableGeometry()
        #
        # self.setMinimumWidth(resolution.width() / 7)
        # self.setMinimumHeight(resolution.height() / 8)

        self.main_widget = Player(self)
        self.resize(800,800)
        self.setCentralWidget(self.main_widget)



    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class Player(QtWidgets.QWidget):

    def __init__(self, parent):
        super(Player, self).__init__(parent)
        print("w:" + str(self.width()) + " h:" + str(self.height()) )

        # self.resize(400,400)
        self.videoframe = Video_frame()

        # print("w:" + str(self.width()) + " h:" + str(self.height()) )

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxlayout)
        # self.videoframe.play()






        # overlay = Overlay(self)




    def test(self):
        print("test")



class Video_frame(QtWidgets.QFrame):
    def __init__(self,parent=None):
        super(Video_frame, self).__init__(parent)

        self.palette = self.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(100, 0, 60))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        # self.clicked.connect(self.say_hello)
        self.mouseReleaseEvent = self.play
        # QObject.connect(self, SIGNAL ('clicked()'), self.say_hello)

    def say_hello(self,event):
        print("Button clicked, Hello!")
        print("w:" + str(self.width()) + " h:" + str(self.height()) )

    def play(self,event):
        print("play")


        # Creation
        self.Media = self.instance.media_new(unicode(
            os.path.join("/home/odo/incoming/xtorrent/", "ps-alex-blake.720.mp4" )))
        self.player.set_media(self.Media)
        # Report the title of the file chosen
        # title = self.player.get_title()
        #  if an error was encountred while retriving the title, then use
        #  filename


        # set the window id where to render VLC's video output
        handle = self.winId()
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.player.set_xwindow(handle)
        elif sys.platform == "win32": # for Windows
            self.player.set_hwnd(handle)
        elif sys.platform == "darwin": # for MacOS
            self.player.set_nsobject(handle)
        # self.OnPlay(None)

        if self.player.play() == -1:
            print("unable to play")



    def on_bouble_click(self):
        print("d_click")

    def on_left_click(self):
        print("L_click")

    def on_right_click(self):
        print("R_click")


class Overlay(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):

        QtWidgets.QGraphicsView.__init__(self, parent=parent)


        self.button = QPushButton("Bt")

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.button)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxlayout)



        # self.scene = QtWidgets.QGraphicsScene(self)
        # self.view = QGraphicsView(self.scene)
        #
        # # self.button = QPushButton("Do test")
        #
        # layout = QVBoxLayout()
        # # layout.addWidget(self.button)
        # layout.addWidget(self)
        # self.setLayout(layout)
        #
        # # self.button.clicked.connect(self.do_test)
        # # self.item = QtWidgets.QGraphicsRectItem(300,400,400,400)
        # # self.scene.addItem(self.item)
        # self.setScene(self.scene)
        #
        # self.setGeometry(0,0,self.parent().parent().width(),self.parent().parent().height())
        # # self.setStyleSheet("background: transparent")
        #
        #
        # self.display_image()


    # def do_test(self):
    #     img = Image.open('folder-html.png')
    #     enhancer = ImageEnhance.Brightness(img)
    #     for i in range(1, 8):
    #         img = enhancer.enhance(i)
    #         self.display_image(img)
    #         QCoreApplication.processEvents()  # let Qt do his work
    #         time.sleep(0.5)

    def display_image(self):
        self.scene.clear()
        # w, h = img.size
        self.imgQ = QtGui.QImage('folder-html.png')  # we need to hold reference to imgQ, or it will crash
        pixMap = QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
        # self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        self.scene.update()




def main():
    app = QtWidgets.QApplication(sys.argv)

    player = Player_Main_Window()
    player.show()
    # player.resize(640, 480)
    # player.Play()

    sys.exit(app.exec_())
if __name__ == '__main__':
    main()

