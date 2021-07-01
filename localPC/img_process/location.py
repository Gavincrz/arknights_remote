import numpy as np
image_dir = "images"

# based on 1440x810 px (width x height)
ref_resolution = (1440,810)

# rect format: ((lefttop_x, lefttop_y),(offset_x, offset_y))
icon_map = {
    "main_screen": {
        "form_team" : ((779, 346), (239, 96))
    },
    "start_screen": {
        "start_icon": ((676, 723), (90, 83))
    },
    "common": {
        
    }
}

icon_cache = {
    "main_screen": {
        "form_team" : None
    },
    "start_screen": {
        "start_icon": None
    }
}

