import numpy as np
import cv2
import math
import os
import logging
from .location import *

logger = logging.getLogger(__name__)


def get_ref_img(screen_name, icon_name):
    # check if the image is already loaded
    if icon_cache[screen_name][icon_name] is not None:
        return icon_cache[screen_name][icon_name]
    else:
        img_path = construct_ref_img_path(screen_name, icon_name)
        loaded_img = cv2.imread(img_path)
        icon_cache[screen_name][icon_name] = loaded_img
        logger.debug(f"Image loaded to cache: {img_path}")
        return loaded_img


def construct_ref_img_path(screen_name, icon_name):
    return os.path.join(image_dir, f"{screen_name}-{icon_name}.png")

def convert_rect(height, width, rect):
    # convert the rect based on real resolution
    # rect format: ((lefttop_x, lefttop_y),(offset_x, offset_y))
    height_ratio = height/ref_resolution[1]
    width_ratio = width/ref_resolution[0]

    return ((math.floor(rect[0][0] * width_ratio), math.floor(rect[0][1] * height_ratio)),
            (math.floor(rect[1][0] * width_ratio), math.floor(rect[1][1] * height_ratio)))

def get_icon_from_img(img, screen_name, icon_name):
    # dump icon to image/ dir
    img_height, img_width = img.shape[:2]
    rect = icon_map[screen_name][icon_name]
    real_rect = convert_rect(img_height, img_width, rect)
    crop_img = crop_image(img, real_rect)

    return crop_img

def dump_icon(img, screen_name, icon_name):
    # dumped icon must have reference size
    img_height, img_width = img.shape[:2]
    if img_height != ref_resolution[1] or img_width != ref_resolution[0]:
        logger.error(f"screenshot does not have ref size when dumpping icon! {img_width}x{img_height}")
        return
    crop_img = get_icon_from_img(img, screen_name, icon_name)

    output_path = construct_ref_img_path(screen_name, icon_name)
    # dump the icon to file
    cv2.imwrite(output_path, crop_img)
    logger.debug(f"Icon dumpped to {output_path}")

def crop_image(img, rect):
    crop_img = img[rect[0][1]: rect[0][1] + rect[1][1], rect[0][0]: rect[0][0] + rect[1][0]]
    return crop_img


def compare_image(img1, img2):
    # resize the image before comparing
    img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)[0, 0]
    return result