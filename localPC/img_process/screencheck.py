import logging
import cv2
from . import imgops 

logger = logging.getLogger(__name__)

def check_icon_exist(img, screen_name, icon_name, threshold=0.8):
    ref_img = imgops.get_ref_img(screen_name, icon_name)
    icon_img = imgops.get_icon_from_img(img, screen_name, icon_name)

    # resize the image to ref size
    compare_coe = imgops.compare_image(icon_img, ref_img)
    logger.debug(f"compare with {icon_name}, result: {compare_coe}")
    return compare_coe > threshold

def check_start_icon(img):
    return check_icon_exist(img, "start_screen", "start_icon")

def check_at_main(img):
    return check_icon_exist(img, "main_screen", "form_team")

def check_navi_bar(img):
    return check_icon_exist(img, "common", "navi_bar")

def check_at_terminal(img):
    return check_icon_exist(img, "terminal_screen", "terminal_icon")

def check_navi_bar_setting(img): 
    # check for the white navi bar, exist in setting and mail screen
    return check_icon_exist(img, "common", "navi_bar_white")

def get_navi_bar_point(img_shape):
    return imgops.get_left_top_corner(img_shape, "common", "navi_bar")

def get_start_icon_point(img_shape):
    return imgops.get_left_top_corner(img_shape, "start_screen", "start_icon")

def get_navi_bar_white_point(img_shape):
    return imgops.get_left_top_corner(img_shape, "common", "navi_bar_white")

def get_terminal_icon_point(img_shape):
    return imgops.get_left_top_corner(img_shape, "main_screen", "terminal_icon")

def find_x_button(img, threshold=0.8):
    # find x button on the top right corner
    # first resize the image to ref size
    img = imgops.resize_screencap_to_ref(img)

    # get rect of top right corner
    rect = imgops.get_top_right_rect(img)

    # find x_button in image
    point, maxVal = imgops.find_image(img, "common", "x_button", rect)

    logger.debug(f"Finding x_button in image, maxVal = {maxVal}, point = {point}")

    return point, maxVal > threshold


# check if current screen contains ep cover
# ep: integer ep number
def find_ep_cover(img, ep, threshold=0.8):
    # first resize the image to ref size
    img = imgops.resize_screencap_to_ref(img)

    # rect use the whole screen
    rect = ((0, 0), (img.shape[1], img.shape[0]))

    # find x_button in image
    point, maxVal = imgops.find_image(img, "ep_cover", f"ep{ep:02d}", rect)
    logger.debug(f"Finding ep{ep:02d} cover with original size, maxVal = {maxVal}")
    
    if maxVal > threshold:
        logger.debug("ep cover found with big cover!")
        return point, True

    # check with small img, big and small image have fixed ratio
    scale_ratio = 354/300

    # scale up the small image and compare again
    width = int(img.shape[1] * scale_ratio)
    height = int(img.shape[0] * scale_ratio)
    dim = (width, height)

    resized = cv2.resize(img, dim)

    point, maxVal = imgops.find_image(resized, "ep_cover", f"ep{ep:02d}", rect)
    logger.debug(f"Finding ep{ep:02d} cover with scaled size, maxVal = {maxVal}")

    if maxVal > threshold:
        logger.debug("ep cover found with small cover!")
        # scale point back to origin
        point = (int(point[0]/scale_ratio), int(point[1]/scale_ratio))
        return point, True

    return point, False
