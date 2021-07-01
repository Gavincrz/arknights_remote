import logging
from . import imgops 

logger = logging.getLogger(__name__)

def check_icon_exist(img, screen_name, icon_name):
    ref_img = imgops.get_ref_img(screen_name, icon_name)
    icon_img = imgops.get_icon_from_img(img, screen_name, icon_name)

    # resize the image to ref size
    compare_coe = imgops.compare_image(icon_img, ref_img)
    logger.debug(f"compare with {icon_name}, result: {compare_coe}")
    return compare_coe > 0.7


def check_at_main(img):
    return check_icon_exist(img, "main_screen", "form_team")

def check_navi_bar(img):
    return check_icon_exist(img, "common", "navi_bar")

def check_navi_bar_setting(img): 
    # check for the white navi bar, exist in setting and mail screen
    return check_icon_exist(img, "common", "navi_bar_white")

def get_navi_bar_point(img_shape):
    return imgops.get_left_top_corner(img_shape, "common", "navi_bar")


def get_navi_bar_white_point(img_shape):
    return imgops.get_left_top_corner(img_shape, "common", "navi_bar_white")

def find_x_button(img):
    # find x button on the top right corner
    # first resize the image to ref size
    img = imgops.resize_screencap_to_ref(img)

    # get rect of top right corner
    rect = imgops.get_top_right_rect(img)

    # find x_button in image
    point, maxVal = imgops.find_image(img, "common", "x_button", rect)

    logger.debug(f"Finding x_button in image, maxVal = {maxVal}, point = {point}")

    return point, maxVal > 0.7