#!/usr/bin/env python3

import sys
import os
from vlc import vlc
from utils.log import Log
from yapvp_constants import YapvpConstants
from pathlib import Path
from utils import utils


class Yapvp_data():

    def __init__(self, debug_level=1):
        self.log = Log()
        self.log.log_level = debug_level

        # write empty config if not provided
        self.user_config_file_path = Path(YapvpConstants.main_home_config_file)

        if not self.user_config_file_path.is_file():
            self.config = YapvpConstants.default_config
            self.write_config_file()

        self.load_config_file()
        self.log.debug(self.config)

    def load_config_file(self):
        self.log.debug("Loading main config file: " + YapvpConstants.main_home_config_file)
        self.config = utils.Utils.load_yaml(self.user_config_file_path, YapvpConstants.default_config)

    def write_config_file(self):
        self.log.debug("Writing default config file: " + YapvpConstants.main_home_config_file)
        utils.Utils.create_path(os.path.dirname(str(self.user_config_file_path)))
        utils.Utils.write_yaml(self.user_config_file_path, self.config)


def main():
    vapvp = Yapvp_data(0)


if __name__ == '__main__':
    main()
