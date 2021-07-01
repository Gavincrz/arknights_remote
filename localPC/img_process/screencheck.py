import logging
from . import imgops 

logger = logging.getLogger(__name__)

def check_icon_exist(img, screen_name, icon_name):
    ref_img = imgops.get_ref_img(screen_name, icon_name)
    icon_img = imgops.get_icon_from_img(img, screen_name, icon_name)

    # resize the image to ref size
    compare_coe = imgops.compare_image(icon_img, ref_img)
    logger.debug(f"compare coe of {icon_name} is {compare_coe}")
    return compare_coe > 0.7


def check_at_main(img):
    return check_icon_exist(img, "main_screen", "form_team")

def check_navi_bar(img):
    return check_icon_exist(img, "common", "navi_bar")

def get_navi_bar_point(img_shape):
    return imgops.get_left_top_corner(img_shape, "common", "navi_bar")

