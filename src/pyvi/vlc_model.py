#!/usr/bin/env python3

from vlc import vlc
import sys
from utils import  log

class VlcModel():
    max_audio_boost = 150
    video_jump_ms = 10000

    def __init__(self):

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.log =  log.SingleLog()

    def set_frame_id(self,frame_id):
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.player.set_xwindow(frame_id)
        elif sys.platform == "win32":  # for Windows
            self.player.set_hwnd(frame_id)
        elif sys.platform == "darwin":  # for MacOS
            self.player.set_nsobject(frame_id)
        # self.OnPlay(None)

    def play(self, file):

        if file is not False:

            self.Media = self.instance.media_new(str(file))
            self.player.set_media(self.Media)

            if self.player.play() == -1:
                self.log.error("unable to play file "+ str(file))

    def play_pause(self):
        self.player.pause()

    def resume(self):
        state = self.player.get_state()
        if str(state) == "State.Paused":
            self.player.pause()

    def vol_up(self):
        curV = self.player.audio_get_volume()
        vol =  curV + 10
        if vol > self.max_audio_boost:
            vol = self.max_audio_boost

        self.player.audio_set_volume(vol)
        self.log.debug("current audio volume: "+str(vol))

    def vol_down(self):
        curV = self.player.audio_get_volume()
        vol =  curV - 10
        if vol <= 0:
            vol = 0

        self.player.audio_set_volume(vol)
        self.log.debug("current audio volume: "+str(vol))

    def video_advance(self,dif = None, max_r=0):
        self.resume()
        max = self.player.get_length()
        if dif is None:
            dif = self.video_jump_ms

        position = self.player.get_time() + dif
        if position >= max and max_r < 4:
            max_r +=1
            self.video_advance(dif/2,max_r)
        else:
            self.player.set_time(position)

    def video_rewind(self):
        self.resume()
        position = self.player.get_time() - self.video_jump_ms
        if position <= 0:
            position = 0
        self.player.set_time(position)




    def test(self):
        print("test ok")