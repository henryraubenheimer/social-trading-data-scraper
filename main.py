# #import constants
# import crawlers
# import parsers
# import time

# # time.sleep(constants.INIT_WAIT)
# # crawlers.crawl_search()

# parsers.parse_files()

import time

time.sleep(5)

import constants
import crawlers

crawlers.crawl_search()

# import time

# time.sleep(5)

# import pyautogui

# SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size() 
# unfiltered_boxes = pyautogui.locateAllOnScreen('screenshots/share position.png', region=(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), grayscale=True)

# for box in unfiltered_boxes:
#     print(box)