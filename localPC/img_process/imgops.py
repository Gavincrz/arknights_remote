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

def resize_screencap_to_ref(img):
    return cv2.resize(img, (ref_resolution[0], ref_resolution[1]))

def compare_image(img1, img2):
    # resize the image before comparing, two image should have the same size
    img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)[0, 0]
    return result


def get_left_top_corner(img_shape, screen_name, icon_name):
    height = img_shape[0]
    width = img_shape[1]

    # choose the lefttop corner of the rect
    rect = icon_map[screen_name][icon_name]
    real_rect = convert_rect(height, width, rect)

    return real_rect[0]


def get_top_right_rect(img):
    width = img.shape[1]
    height = img.shape[0]
    return ((math.floor(width/2), 0), (math.floor(width/2), math.floor(height/2)))

def find_image(img, screen_name, icon_name, search_rect):
    # find icon in the image, two image do not need to have the same size
    # https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html
    # load the icon image
    ref_img = get_ref_img(screen_name, icon_name)
    
    # get cropped area
    crop_area = crop_image(img, search_rect)

    # find the icon
    result = cv2.matchTemplate(crop_area, ref_img, cv2.TM_CCOEFF_NORMED)

    # localize the minimum and maximum values
    _minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)

    # best match is the max value
    # return the point and maxval 
    # maxLoc is the relative loc of the cropped img, calculate the original loc
    point = (search_rect[0][0] + maxLoc[0], search_rect[0][1] + maxLoc[1])

    return point, maxVal

# find all appearance of ref_img
def find_templates_in_img(img, ref_img, threshold):
    result = cv2.matchTemplate(img, ref_img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    print(loc)
    print(result[loc])
    print(len(loc[0]))
    return loc


# copy from https://github.com/ninthDevilHAUNSTER/ArknightsAutoHelper
def remove_holes(img):
    # 去除小连通域 
    # findContours 只能处理黑底白字的图像, 所以需要进行一下翻转
    contours, hierarchy = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        # 计算区块面积
        area = cv2.contourArea(contours[i])
        if area < 10:
            # 将面积较小的点涂成白色，以去除噪点
            cv2.drawContours(img, [contours[i]], 0, 255, -1)

def process_tag_img_for_ocr(img):
    # convert to grey
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threads hold and inverse (for background other than white)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    if img[0, 0] < 127:
        img = ~img
    
    # remove holes
    remove_holes(img)

    return img