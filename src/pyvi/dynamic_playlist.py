#!/usr/bin/env python3

import sys
import os
from utils.log import SingleLog
from pyvi.constants import PyviConstants
from pathlib import Path
import magic
import pprint


class PyviDynamicPlaylist():
    # key value dict holding play order - file
    dynamic_playlist = {}
    dynamic_playlist_max_val = -1
    dynamic_playlist_min_val = 0
    dynamic_playlist_current_val = 0

    def __init__(self, config):

        self.config = config
        if len(sys.argv) > 1:
            path = sys.argv[1]
        else:
            path = ""

        self.log = SingleLog()

        # write empty config if not provided
        self.user_config_file_path = Path(PyviConstants.main_home_config_file)

        self.dest = path
        self.start()

    def start(self):
        dest = self.dest
        self.log.debug("starting with destination: " + str(dest))

        dest_Path = Path(dest)
        if dest_Path.is_file():
            file_index_base = dest_Path
            base_path = dest_Path.parent
        elif dest_Path.is_dir():
            base_path = dest_Path
            file_index_base = False
        else:
            self.log.error(str(dest) + " is not a valid path or file")
            return False

        self.log.debug("using: " + str(base_path) + " as base path")
        sorted_destination = sorted(os.scandir(base_path), key=lambda x: x.name, reverse=False)
        for entry in sorted_destination:
            if not entry.name.startswith('.'):
                abs_path = os.path.join(base_path, entry.name)
                if Path(abs_path).is_file():
                    if self.is_video_file(abs_path):
                        self.dynamic_playlist_max_val += 1
                        self.dynamic_playlist[self.dynamic_playlist_max_val] = abs_path

                        if file_index_base is not False and str(file_index_base) == str(abs_path):
                            self.dynamic_playlist_current_val = self.dynamic_playlist_max_val

    def is_video_file(self, file):
        if self.config["trust_video_extensions"] is True:
            self.log.debug("try to find out file type based on extension for: " + file)
            filename, extension = os.path.splitext(file)
            extension = extension[1:].lower().strip()

            if len(extension) > 0:
                if extension in PyviConstants.video_types_extensions:
                    return True
                else:
                    return False
            elif len(extension) == 0 and self.config["only_check_video_extension"] is False:
                return self.is_vide_based_on_mime(file)
        else:
            return self.is_vide_based_on_mime(file)

    def is_vide_based_on_mime(self, file):
        # self.log.debug("try to find out file type based on magic byte for: "+ file)
        mime = magic.Magic(mime=True)
        m = mime.from_file(file).strip()
        m = m.split("/")
        m = m[0]

        self.log.debug("found mime based type: " + m + " for:" + file)
        if m == "video":
            return True
        else:
            return False

    def next(self):
        """
        return next video to play based on:
        - same level has a video
        - if same dir does not contain a video, check sub folder (alphabetical order)
        - if current dir does not contain a video or sub folder, go one level up2
        Note, add to sortec cache
        :return:
        """

        if self.dynamic_playlist_current_val < self.dynamic_playlist_max_val:
            self.dynamic_playlist_current_val += 1
            return self.dynamic_playlist[self.dynamic_playlist_current_val]
        else:
            return False

    def previous(self):
        """
        return next video to play based on:
        - same level has a video
        - if same dir does not contain a video, check sub folder (alphabetical order)
        - if current dir does not contain a video or sub folder, go one level up2
        :return:
        """
        if self.dynamic_playlist_current_val > self.dynamic_playlist_min_val:
            self.dynamic_playlist_current_val -= 1
            return self.dynamic_playlist[self.dynamic_playlist_current_val]
        else:
            return False

    def current(self):
        if self.dynamic_playlist_current_val >= self.dynamic_playlist_min_val and \
            self.dynamic_playlist_current_val <= self.dynamic_playlist_max_val :
            return self.dynamic_playlist[self.dynamic_playlist_current_val]
        else:
            return False

    def get_dynamic_playlist(self):
        return {
            "items": self.dynamic_playlist,
            "current": self.dynamic_playlist_current_val,
            "max": self.dynamic_playlist_max_val,
            "min": self.dynamic_playlist_min_val
        }


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = None

    yapvp = Yapvp_data(dest=path, debug_level=0)
    pp = pprint.PrettyPrinter(indent=3)
    pp.pprint(yapvp.get_dynamic_playlist())

    print("current")
    for e in range(1):
        print(str(e) + ": " + str(yapvp.current()))

    print("next")
    for i in range(10):
        print(str(i) + ": " + str(yapvp.next()))

    print("previous")
    for j in reversed(range(9)):
        print(str(j) + ": " + str(yapvp.previous()))

    print("current")
    for e in range(3):
        print(str(e) + ": " + str(yapvp.current()))


if __name__ == '__main__':
    main()
