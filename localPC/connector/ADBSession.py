import logging
import socket
import numpy as np
import cv2

import config
from ppadb.client import Client as AdbClient

logger = logging.getLogger(__name__)


class ADBSession():
    def __init__(self, server, serial=None):
        self.server = server
        self.client = AdbClient(host=self.server[0], port=self.server[1])

        if self.client is not None:
            logger.debug(f"Create to adb client succssfully! {self.server[0]}:{self.server[1]}")

        devices = self.client.devices()
        if len(devices) > 0:
            self.device = devices[0]
            logger.debug(f"{len(devices)} devices found! Connect the first one: {self.device.serial}")
        else:
            logger.error("No device found")

        self.get_screen_size()

    def shell_raw(self, cmd):
        # overwrite the shell function so that it returns raw byte instead of utf-8 decoded
        conn = self.device.create_connection(timeout=None)
        cmd = "exec:{}".format(cmd)
        conn.send(cmd)
        result = conn.read_all()
        conn.close()
        return result

    def get_screen_size(self):
        image = self.get_screenshot()
        self.width, self.height, self.channel = image.shape
        logger.debug(f"Screen size is ({self.height}, {self.width}, {self.channel})")

    def exec_cmd(self, cmd):
        """ run command in adb shell """
        return self.device.shell(cmd)

    def list_devices(self):
        devices = self.client.devices()
        for device in devices:
            print(device.serial)

    def get_screenshot(self):
        # take screenshot and convert to cv2 image
        data = self.shell_raw("screencap -p")
        np_image = np.array(data)
        image = cv2.imdecode(np_image, 1)
        logger.debug(f"Get screenshot of size {image.shape}")
        return image

    def tap_screen(self, x, y):
        command = f"input tap {x} {y}"
        self.exec_cmd(command)
        logger.debug(f"Tap screen: ({x},{y})")
    