#!/usr/bin/env python3

import os
import sys
from pyvi.constants import PyviConstants
from pyvi.vlc_model import VlcModel
from pyvi.dynamic_playlist import PyviDynamicPlaylist

from utils.singleton import Singleton
from pathlib import Path
from utils import utils, log

from PySide2 import QtCore


class pyviActions:

    def __init__(self, config):
        defaults = {
            "f": "toggle_fullscreen",
            "g": "play",
            "{space}": "toggle_play_pause",
            "{esc}": "exit",
            "{up}": "volume_up",
            "{down}": "volume_down",
            "{right}": "video_advance",
            "{left}": "video_rewind",
            "{next}": "play_next",
            "{prior}": "play_prev",
        }
        if "keys" in config.keys():
            config["keys"] = utils.Utils.merge_objects(defaults, config["keys"])
        else:
            config["keys"] = defaults

        self.config = config
        self.log = log.SingleLog()

    def qevent_to_key(self,ev):
        self.log.debug("key press mod:" + str(ev.nativeModifiers()) + " native virt key " + str(ev.nativeVirtualKey())+ " key: "+str(ev.key()))

        if ev.nativeModifiers() in PyviConstants.key_modifiers.keys():
            modifier = PyviConstants.key_modifiers[ev.nativeModifiers()]
            if modifier == "none":
                modifier = ""
        else:
            modifier = ""

        native_virt_key = ev.nativeVirtualKey()
        if native_virt_key in PyviConstants.native_key_codes.keys():
            key = PyviConstants.native_key_codes[native_virt_key]
        elif ev.text() is not "":
            key = ev.text()
        else:
            key = False

        if key is not False:
            if len(modifier) > 1:
                keys = modifier.split("+")
            else:
                keys = []
            keys.append(key)
            keys = sorted(keys, key=str.lower)

            key_press_string= '+'.join(str(x) for x in keys)
            # print(key_press_string)
            return key_press_string
        else:
            return False

    def get_key_action(self,ev):

        key_string = self.qevent_to_key(ev)
        self.log.debug("pressed keys string: "+str(key_string))

        action_keys = self.config["keys"].keys()
        if key_string is not False and key_string in action_keys:
            return self.config["keys"][key_string]
        else:
            return False



class PyviController(metaclass=Singleton):
    main_window = None
    central_widget = None
    left_click_timer = None
    is_full_screen = False
    video_frame_model = None
    dynamic_playlist = None

    def __init__(self):

        self.log = log.SingleLog(0)

        # write empty config if not provided
        self.user_config_file_path = Path(PyviConstants.main_home_config_file)

        # deal with user config
        if not self.user_config_file_path.is_file():
            self.config = PyviConstants.default_config
            self.write_config_file()

        self.load_config_file()

        self.actions = pyviActions(self.config)



    def load_config_file(self):
        self.log.debug("Loading main config file: " + PyviConstants.main_home_config_file)
        self.config = utils.Utils.load_yaml(self.user_config_file_path, PyviConstants.default_config)

    def write_config_file(self):
        self.log.debug("Writing default config file: " + PyviConstants.main_home_config_file)
        utils.Utils.create_path(os.path.dirname(str(self.user_config_file_path)))
        utils.Utils.write_yaml(self.user_config_file_path, self.config)

    def start(self):

        # start the dynamic playlist
        self.dynamic_playlist = PyviDynamicPlaylist(self.config)

        # start vlc instance
        self.video_frame_model = VlcModel()
        self.video_frame_model.set_frame_id(self.video_fram_id)
        self.video_frame_model.play(self.dynamic_playlist.current())

    def on_video_frame_load(self, frame_id):
        self.video_fram_id = frame_id

    def on_main_window_key_release(self, ev):
        func = self.actions.get_key_action(ev)
        if func is not False :
            # try:
                eval("self."+func+"()")
            # except AttributeError:
            #     self.log.error("Controller action: "+ func +" does not exist")

    def on_main_window_key_press(self, ev):
        pass
        # print("key press text:" + str(ev.text()) + " native virt key " + str(ev.nativeVirtualKey()))
        # keycode = event.GetKeyCode()
        # print (keycode)
        # if keycode == wx.WXK_SPACE:
        #     print ("you pressed the spacebar!")
        # event.Skip()
        #

    def on_video_click_press(self, ev):
        self.left_click_timer = QtCore.QTimer()
        self.left_click_timer.timeout.connect(self.on_single_left_click)
        self.left_click_timer.start(200)

    def on_video_click_release(self, ev):
        # print("L_click release")
        pass

    def on_video_double_click(self, ev):
        self.left_click_timer.stop()
        self.toggle_fullscreen()

    def on_single_left_click(self):
        print("single click")

        self.left_click_timer.stop()

        next = self.dynamic_playlist.next()
        if next is not False:
            self.log.debug("play: " + str(next))
            self.video_frame_model.play(str(next))

    def toggle_fullscreen(self):
        if self.is_full_screen is False:
            self.is_full_screen = True
            self.main_window.showFullScreen()
        else:
            self.is_full_screen = False
            self.main_window.showNormal()

    def exit(self):
        sys.exit(0)

    def volume_up(self):
        self.video_frame_model.vol_up()

    def volume_down(self):
        self.video_frame_model.vol_down()

    def video_advance(self):
        r = self.video_frame_model.video_advance()

    def video_rewind(self):
        r = self.video_frame_model.video_rewind()

    def play_next(self):
        nextv = self.dynamic_playlist.next()
        if nextv is not False:
            self.video_frame_model.play(nextv)

    def play_prev(self):
        pre = self.dynamic_playlist.previous()
        if pre is not False:
            self.video_frame_model.play(pre)

    def toggle_play_pause(self):
        self.video_frame_model.play_pause()
