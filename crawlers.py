import pandas as pd
from PIL import ImageChops
import pyautogui
import time

import constants
import data_extractors

# crawl a page detailing purchases for a specific share by a specific investor
def crawl_share(extractor):

    prev_im = pyautogui.screenshot()

    # scroll to shares
    init_scrolls = constants.SHARE_SCREEN_HEADER // constants.SCROLL_CLICK_LENGTH
    pyautogui.scroll(-init_scrolls)
    time.sleep(constants.SCROLL_WAIT)

    # take the first screenshot
    counter = 0
    scrolls = ( constants.SCREEN_HEIGHT - constants.INVESTOR_BANNER_HEIGHT ) // constants.SCROLL_CLICK_LENGTH
    im = pyautogui.screenshot(region=(constants.SIDEBAR_WIDTH, constants.INVESTOR_BANNER_HEIGHT, 
                        constants.SCREEN_WIDTH-constants.SIDEBAR_WIDTH-10, constants.SCREEN_HEIGHT-constants.INVESTOR_BANNER_HEIGHT))

    # continue taking screenshots while end of list has not been reached
    while ImageChops.difference(im.convert('RGB'), prev_im.convert('RGB')).getbbox():

        df = pd.DataFrame(extractor.analyse_shares(im))
        df.to_csv('csvs/test'+str(counter)+'.csv', index=False)
        counter += 1

        pyautogui.scroll(-scrolls)
        time.sleep(constants.SCROLL_WAIT)

        prev_im = im.copy()
        im = pyautogui.screenshot(region=(constants.SIDEBAR_WIDTH, constants.INVESTOR_BANNER_HEIGHT, 
                        constants.SCREEN_WIDTH-constants.SIDEBAR_WIDTH-10, constants.SCREEN_HEIGHT-constants.INVESTOR_BANNER_HEIGHT))

def crawl_portfolio(extractor):
    
    scrolls = 2 # how many times there has been scrolled
    indent = 0 # how far the topmost relevant stock is from the top

    while True:

        shares_clicked = 0 # how many shares on the current screen have been clicked

        # click shares until last one has been reached
        while constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 1 ) * constants.SHARE_HEIGHT ) < constants.SCREEN_HEIGHT:

            pyautogui.scroll(-scrolls)
            time.sleep(constants.SCROLL_WAIT)

            # click stock
            if not pyautogui.pixelMatchesColor(200, constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 0.5 ) * constants.SHARE_HEIGHT ), (255, 255, 255)):
                return
            pyautogui.click(200, constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 0.5 ) * constants.SHARE_HEIGHT ))
            time.sleep(constants.LOAD_PAGE_WAIT)

            crawl_share(extractor)

            # go back to portfolio page
            with pyautogui.hold('alt'):
                pyautogui.press(['left'])
            time.sleep(constants.LOAD_PAGE_WAIT)

            shares_clicked += 1
            
        # calculate new indent of topmost stock
        relevant_bottom = constants.SCREEN_HEIGHT - ( constants.SCREEN_HEIGHT - ( constants.INVESTOR_BANNER_HEIGHT + indent ) ) % constants.SHARE_HEIGHT
        indent = (relevant_bottom - constants.INVESTOR_BANNER_HEIGHT ) - constants.SCROLL_CLICK_LENGTH
        
        pyautogui.scroll(scrolls)
        scrolls += 1

def crawl_people():
    pass