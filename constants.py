import os
import time

import pyautogui

INFINITE_SCROLL_WAIT = 0.5
INFINITE_SCROLL_SAFETY_WAIT = 5
LOAD_PAGE_WAIT = 1
SCROLL_WAIT = 1

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size() 
SCROLL_X = SCREEN_WIDTH
SCROLL_Y = 0.75*SCREEN_HEIGHT
INITIAL_TICKS_TILL_DOWNLOAD = 1
TICKS_TILL_DOWNLOAD = 7

# a function that calculates the scroll distance in pixels
def calibrate():

    width, height = pyautogui.size()

    pyautogui.scroll(-1, x=SCROLL_X, y=SCROLL_Y) # to get over the disappearing search panel
    time.sleep(SCROLL_WAIT)

    im = pyautogui.screenshot(region=(int(0.25*width), int(0.75*height), int(0.5*width), int(0.25*height)))
    im.save('screenshots/scroll distance test.png')

    pyautogui.scroll(-1, x=SCROLL_X, y=SCROLL_Y)
    time.sleep(SCROLL_WAIT)

    new_location = pyautogui.locateOnScreen(im)

    pyautogui.scroll(2)
    time.sleep(SCROLL_WAIT)

    return int(0.75*height) - new_location.top

SCROLL_CLICK_LENGTH = 120
SIDEBAR_WIDTH = 136
INVESTOR_HEIGHT = 63
SEARCH_BANNER_HEIGHT = 280
SEARCH_SCREEN_FIRST_INDENT = 191
SEARCH_SCREEN_HEADER = 423
PORTFOLIO_BUTTON_X = 740
PORTFOLIO_BUTTON_Y = 360
INVESTOR_BANNER_HEIGHT = 250
SHARE_HEIGHT = 57

HTML_SAVE_DIR = "/home/"+os.getlogin()+"/Downloads"



INVESTOR_MATCH_CONFIDENCE = 0.6
MIN_BUTTON_OVERLAP = 0.3
SCROLL_DISTANCE = calibrate()
SHARE_POSITION_MATCH_CONFIDENCE = 0.4