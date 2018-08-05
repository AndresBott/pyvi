#!/usr/bin/env python
import os


class PyviConstants():
    project_name = "yapvp"

    user_home = os.environ["HOME"]
    config_dir = user_home + "/.config/"+project_name
    main_home_config_file = config_dir +"/"+ project_name+".config.yaml"
    video_types_extensions = [
        "mp4",
        "mov",
        "mkv",
        "wmv",
        "ogv",
        "ogg",
        "flv",
    ]

    default_config = {
        "trust_video_extensions":True,
        "only_check_video_extension":False
    }

    key_modifiers={
        16: "none",
        17: "[shift]",
        20: "[ctrl]",
        21: "[ctrl]+[shift]",
        24: "[alt]",
        25: "[alt]+[shift]",
        81: "[alt]+[cmd]",
        144: "[altgr]",
        145: "[shift]+[altgr]",
        80: "[cmd]",
    }

    native_key_codes={
        32: "{space}",
        65307: "{esc}",
        65470: "{f1}",
        65366: "{next}",
        65365: "{prior}",
        65362: "{up}",
        65364: "{down}",
        65363: "{right}",
        65361: "{left}",

    }