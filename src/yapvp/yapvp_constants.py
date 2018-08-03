#!/usr/bin/env python
import os


class YapvpConstants():
    project_name = "yapvp"

    user_home = os.environ["HOME"]
    config_dir = user_home + "/.config/"+project_name
    main_home_config_file = config_dir +"/"+ project_name+".config.yaml"

    default_config = {
        "test": True
    }
