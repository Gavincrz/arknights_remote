import logging
import socket

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


    def exec_cmd(self, cmd):
        """ run command in adb shell """
        return self.device.shell(cmd)

    def list_devices(self):
        devices = self.client.devices()
        for device in devices:
            print(device.serial)

    