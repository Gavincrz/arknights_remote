import logging
import socket
from ppadb.client import Client as AdbClient

logger = logging.getLogger(__name__)


def dump_output(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        print(data.decode('utf-8'))
    connection.close()


class ADBSession():
    def __init__(self, server=None):
        if server is None:
            server = ('127.0.0.1', 5037) # default adb port
        self.server = server
        self.client = AdbClient(host=server[0], port=server[1])

        if self.client is not None:
            logger.debug(f"Create to adb client succssfully! {server[0]}:{server[1]}")

        devices = self.client.devices()
        if len(devices) > 0:
            self.device = devices[0]
            logger.debug(f"{len(devices)} devices found! Connect the first one: {self.device.serial}")
        else:
            logger.error("No device found")

    def test_shell(self):
        self.device.shell("echo hello world !", handler=dump_output)
        self.device.shell("ls -la", handler=dump_output)

    def list_devices(self):
        devices = self.client.devices()
        for device in devices:
            print(device.serial)

    