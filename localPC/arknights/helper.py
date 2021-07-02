import logging
import sys
import time
import re
import config
from connector.ADBSession import ADBSession
from img_process import screencheck as screenCK
from img_process import imgops
from img_process import location

logger = logging.getLogger(__name__)

SHORT_WAIT_TIME = 1
LONG_WAIT_TIME = 2
LONG_LONG_WAIT_TIME = 5


def get_ep_from_stage(stage_str):
    # return an integer episode number
    # get the first part
    part1 = stage_str.split("-")[0]
    # find the first integer in str
    first_digit = re.search(r"\d", part1).start()
    return int(part1[first_digit:])

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
        # refresh the screen size
        self.get_screenshot()

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


    # update screen size everytime capturing the screen
    def get_screenshot(self):
        img = self.sess.get_screenshot()
        self.screen_shape = img.shape
        return img


    def back_to_main(self):
        logger.info("Go back to main page...")
        retry_count = 0 # reset retry_count after an operation
        while True:
            img = self.get_screenshot()
            # check if already at main page
            if screenCK.check_at_main(img):
                logger.info("Current page is the main page.")
                return True
            # keep press back button if find navigation bar
            if screenCK.check_navi_bar(img):
                self.tap_back_button(img.shape)
                logger.debug("navigation bar (black) tapped.")
                retry_count = 0
                time.sleep(SHORT_WAIT_TIME)
                continue
            # check if at setting or mail page
            if screenCK.check_navi_bar_setting(img):
                self.tap_back_button_white(img.shape)
                logger.debug("navigation bar (white) tapped.")
                retry_count = 0
                time.sleep(SHORT_WAIT_TIME)
                continue
            # check if x button exist (notice and calender screen)
            point, exist = screenCK.find_x_button(img)
            if exist:
                # tap the x button to close the window
                self.sess.tap_screen(point)
                logger.debug("close button tapped.")
                time.sleep(SHORT_WAIT_TIME)
                retry_count = 0
                continue
            # enter main from start screen
            if screenCK.check_start_icon(img):
                self.tap_start_icon_on_start_screen(img.shape)
                logger.debug("start icon on start screen tapped.")
                retry_count = 0
                time.sleep(LONG_WAIT_TIME)
                continue
            else:
                # handle base_exit screen and other dialog
                retry_count += 1
                if retry_count > 10:
                    logger.error(f"Can not exit Unknown screen!")
                    break
                logger.debug(f"Unknown screen, retry count = {retry_count}")
                time.sleep(LONG_LONG_WAIT_TIME)
        return False

    def enter_terminal_screen(self):
        # go to main page, then terminal page
        self.back_to_main()
        # make sure we are at main page after 5s TODO: handle reloading screen
        time.sleep(LONG_LONG_WAIT_TIME)
        self.back_to_main()

        self.sess.tap_screen(screenCK.get_terminal_icon_point(self.screen_shape))
        time.sleep(SHORT_WAIT_TIME)
        img = self.get_screenshot()
        if screenCK.check_at_terminal(img):
            logger.info("Enter terminal screen.")
            return True
        else:
            logger.error("Enter teriminal failed!")
            return False

    def enter_main_story_part(self, ep):
        # check which part the ep belongs to
        # TODO: we assume there's only 2 parts, may need to change after update
        img = self.get_screenshot()
        if ep in location.main_story_part1_episodes:
            # goto part 1 page
            # check if icon exist
            if screenCK.check_icon_exist(img, "main_story", "part1_icon"):
                self.sess.tap_screen(imgops.get_left_top_corner(self.screen_shape, "main_story", "part1_icon"))
                time.sleep(SHORT_WAIT_TIME)
            logger.info("Enter main story part1.")
        elif ep in location.main_story_part2_episodes:
            if screenCK.check_icon_exist(img, "main_story", "part2_icon"):
                self.sess.tap_screen(imgops.get_left_top_corner(self.screen_shape, "main_story", "part2_icon"))
                time.sleep(SHORT_WAIT_TIME)
            logger.info("Enter main story part2.")
        else:
            logger.error(f"Unknown main story stage {stage}")
            return False
        return True

    def enter_episode_map(self, ep):
        # enter episode map
        swipe_count = 0
        # check if current screen contain the ep cover, if not, swipe to left, 4 in total
        while swipe_count < 5:
            img = self.get_screenshot()
            point, ret = screenCK.find_ep_cover(img, ep)
            if ret:
                self.tap_screen(point)
                time.sleep(LONG_WAIT_TIME)
                logger.info(f"Enter episode {ep}")
                return True
            # swipe to left a little
            self.swipe_to_left_short()
            logger.debug(f"Swipe to left to find ep cover, swipe count = {swipe_count}")
            swipe_count += 1
        logger.error("Episode cover not found.")
        return False

    def goto_main_stage_from_ep_map(self, stage):
        pass

    def goto_main_stage(self, stage):
        # enter main story screen
        self.sess.tap_screen(imgops.get_left_top_corner(self.screen_shape, "terminal_screen", "main_icon"))
        time.sleep(SHORT_WAIT_TIME)
        logger.info("Enter main story screen.")

        ep = get_ep_from_stage(stage)
        ret = self.enter_main_story_part(ep)
        if not ret:
            return False
        
        ret = self.enter_episode_map(ep)
        if not ret:
            return False

        # find stage
        self.goto_main_stage_from_ep_map(stage)

    def cmd_battle_main(self, stage, count):
        ret = self.goto_main_stage(stage)

        
        

        


    def cmd_battle_resource(self, stage, count):
        self.sess.tap_screen(imgops.get_left_top_corner(self.screen_shape, "terminal_screen", "resource_icon"))
        time.sleep(SHORT_WAIT_TIME)
        logger.info("Enter daily resource screen.")
        pass

    # battle type: string: main/resource
    # stage: string: e.g. AP-5, 1-7, PR-A-2
    # count: number of times to enter the battle
    def cmd_battle(self, battle_type, stage, count=1):
        # enter terminal page
        # TODO: error handling
        self.enter_terminal_screen()
        time.sleep(SHORT_WAIT_TIME)

        if battle_type == "main":
            self.cmd_battle_main(stage, count)
        elif battle_type == "resource":
            self.cmd_battle_resource(stage, count)
        else:
            logger.error(f"Unknown battle type: {battle_type}, please choose main/resource!")

    def tap_screen(self, point):
        self.sess.tap_screen(point)

    def tap_back_button(self, img_shape):
        self.sess.tap_screen(screenCK.get_navi_bar_point(img_shape))

    def tap_back_button_white(self, img_shape):
        self.sess.tap_screen(screenCK.get_navi_bar_point(img_shape))

    def tap_start_icon_on_start_screen(self, img_shape):
        self.sess.tap_screen(screenCK.get_start_icon_point(img_shape))

    def swipe_to_left_short(self):
        # swipe to left means swipe right
        # choose the middle point as start point
        origin = (self.screen_shape[1]/2, self.screen_shape[0]/2)
        # swipe right for 1/4 screen
        movement = (self.screen_shape[1]/4, 0)
        self.sess.touch_swipe(origin, movement)

    def swipe_to_right_short(self):
        origin = (self.screen_shape[1]/2, self.screen_shape[0]/2)
        movement = (-self.screen_shape[1]/4, 0)
        self.sess.touch_swipe(origin, movement)

    def swipe_to_left_middian(self):
        origin = (self.screen_shape[1]/2, self.screen_shape[0]/2)
        movement = (self.screen_shape[1]/2, 0)
        self.sess.touch_swipe(origin, movement)

    def swipe_to_right_middian(self):
        origin = (self.screen_shape[1]/2, self.screen_shape[0]/2)
        movement = (-self.screen_shape[1]/2, 0)
        self.sess.touch_swipe(origin, movement)

    def test(self):
        # storage button: 1337, 738
        self.sess.tap_screen((1337, 738))
    

