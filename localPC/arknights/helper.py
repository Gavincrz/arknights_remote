import logging
import sys
import config
from connector.ADBSession import ADBSession
logger = logging.getLogger(__name__)


class ArkHelper():
    def __init__(self):
        self.sess = ADBSession(config.ADB_SERVER)
        self.get_uname()

    def focus_game(self):
        # make sure arknights is the current focused window
        logger.debug("Try to launch the game ...")
        if not self.is_current_focus():
            self.start_game()
        logger.info("Arknights started!")

    def start_game(self):
        ret = self.sess.exec_cmd(f"am start -n {config.ARKNIGHTS_PKG_NAME}/{config.ARKNIGHTS_ACT_NAME}")
        logger.debug(ret.strip())

    def is_current_focus(self):
        # check if arknights is the current focused window
        logger.debug("Checking if Arknights started ...")
        result = self.sess.exec_cmd("dumpsys window windows | grep mCurrentFocus")
        logger.debug(result.strip())
        if config.ARKNIGHTS_PKG_NAME_BILIBILI in result:
            logger.debug("Arknights is launched and is the focused one!")
            return True
        else:
            logger.debug("Arknights is not the current focused window.")
            return False

    def get_uname(self):
        logger.debug(f"Device info: {self.sess.exec_cmd('uname -r').strip()}")


    def get_screenshot(self):
        img = self.sess.get_screenshot()
        return img

    def test(self):
        # storage button: 1337, 738
        self.sess.tap_screen(1337, 738)
    
