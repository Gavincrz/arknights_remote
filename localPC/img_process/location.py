import numpy as np
image_dir = "images"

# based on 1440x810 px (width x height)
ref_resolution = (1440,810)

# rect format: ((lefttop_x, lefttop_y),(offset_x, offset_y))
icon_map = {
    "main_screen": {
        "form_team" : ((779, 346), (239, 96)),
        "terminal_icon": ((1019, 136), (147, 87))
    },
    "start_screen": {
        "start_icon": ((676, 723), (90, 83))
    },
    "terminal_screen": {
        "terminal_icon": ((39, 705), (119, 90)),
        "main_icon": ((274, 728), (64, 55)),
        "resource_icon": ((898, 730), (51, 48)),

    },
    "main_story": {
        "part1_icon": ((131, 137), (52, 31)),
        "part2_icon": ((133, 570), (49, 31))
    },
    "common": {
        "navi_bar": ((25, 18),(391, 50)),
        "navi_bar_white": ((42, 32),(57, 36)),
        "x_button": ((1373, 42), (39, 42))  
    },
    "ep_cover": { # only used for dump
        "ep00": ((890, 240), (330, 330)),
        "ep01": ((890, 240), (330, 330)),
        "ep02": ((890, 240), (330, 330)),
        "ep03": ((890, 240), (330, 330)),
        "ep04": ((890, 240), (330, 330)),
        "ep05": ((890, 240), (330, 330)),
        "ep06": ((890, 240), (330, 330)),
        "ep07": ((890, 240), (330, 330)),
        "ep08": ((890, 240), (330, 330))
    }

}

# load image into icon_cache to avoid redundant disk I/O
icon_cache = {
    "main_screen": {
        "form_team" : None,
        "terminal_icon": None
    },
    "start_screen": {
        "start_icon": None
    },
    "terminal_screen": {
        "terminal_icon": None,
        "main_icon": None,
        "resource_icon": None
    },
    "main_story": {
        "part1_icon": None,
        "part2_icon": None
    },
    "common": {
        "navi_bar": None,
        "navi_bar_white": None,
        "x_button": None
    },
    "ep_cover": { 
        "ep00": None,
        "ep01": None,
        "ep02": None,
        "ep03": None,
        "ep04": None,
        "ep05": None,
        "ep06": None,
        "ep07": None,
        "ep08": None
    }
}

main_story_part1_episodes = [0, 1, 2, 3]
main_story_part2_episodes = [4, 5, 6, 7, 8]


main_stage_list = [
    ["0-1", "0-2", "0-3", "0-4", "0-5", "0-6", "0-7", "0-8", "0-9", "0-10", "0-11"], # stage 0
    [], # stage 1
    [], # stage 2
    [], # stage 3
    [], # stage 4
    [], # stage 5
    [], # stage 6
    [], # stage 7
    [], # stage 8
]

