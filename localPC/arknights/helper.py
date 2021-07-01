import logging
import sys
import time
import config
from connector.ADBSession import ADBSession
from img_process import screencheck as screenCK

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

    def back_to_main(self):
        logger.info("Go back to main page...")
        while True:
            img = self.sess.get_screenshot()
            # check if already at main page
            if screenCK.check_at_main(img):
                logger.info("Current page is the main page.")
                break
            # keep press back button if find navigation bar
            if screenCK.check_navi_bar(img):
                self.tap_back_button(img.shape)
                logger.debug("navigation bar (black) tapped.")
                time.sleep(0.5)
                continue
            # check if at setting or mail page
            if screenCK.check_navi_bar_setting(img):
                self.tap_back_button_white(img.shape)
                logger.debug("navigation bar (white) tapped.")
                time.sleep(0.5)
                continue
            # check if x button exist (notice and calender screen)
            point, exist = screenCK.find_x_button(img)
            if exist:
                # tap the x button to close the window
                self.sess.tap_screen(point)
                logger.debug("close button tapped.")
                time.sleep(0.5)
                continue
            else:
                # handle base_exit screen and other dialog
                time.sleep(0.5)
            

    def tap_back_button(self, img_shape):
        self.sess.tap_screen(screenCK.get_navi_bar_point(img_shape))

    def tap_back_button_white(self, img_shape):
        self.sess.tap_screen(screenCK.get_navi_bar_point(img_shape))

    def test(self):
        # storage button: 1337, 738
        self.sess.tap_screen((1337, 738))
    

