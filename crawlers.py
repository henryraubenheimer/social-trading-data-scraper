import pathlib
import pyautogui
import shutil
import time

import constants



# crawl the page detailing purchases for a specific share by a specific investor
def crawl_share():
    pass



# crawl the page detailing the portfolio for a specific investor
def crawl_portfolio():

    click_link(constants.PORTFOLIO_BUTTON_X, constants.PORTFOLIO_BUTTON_Y)

    scrolls = 2 # how many times there has been scrolled
    indent = 30 # how far the topmost relevant stock is from the top

    processing = True
    while processing:

        shares_clicked = 0 # how many shares on the current screen have been clicked

        # click shares until last one has been reached
        while constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 1 ) * constants.SHARE_HEIGHT ) < constants.SCREEN_HEIGHT:

            scroll(-scrolls, False)

            # click stock
            if not pyautogui.pixelMatchesColor(200, round(constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 0.5 ) * constants.SHARE_HEIGHT )), (255, 255, 255)):
                processing = False
                break
            click_link(200, round(constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 0.5 ) * constants.SHARE_HEIGHT )))

            crawl_share()

            go_back()

            shares_clicked += 1
            
        # calculate new indent of topmost stock
        relevant_bottom = constants.SCREEN_HEIGHT - ( constants.SCREEN_HEIGHT - ( constants.INVESTOR_BANNER_HEIGHT + indent ) ) % constants.SHARE_HEIGHT
        indent = (relevant_bottom - constants.INVESTOR_BANNER_HEIGHT ) - constants.SCROLL_CLICK_LENGTH
        
        scroll(scrolls, False)
        scrolls += 1

    go_back()



# crawl the page listing investor search results
def crawl_search():

    investors_clicked = 0

    # click investors until last one has been reached before scrolling
    while constants.SEARCH_SCREEN_HEADER + ( ( investors_clicked + 1 ) * constants.INVESTOR_HEIGHT ) < constants.SCREEN_HEIGHT:

        click_link(200, constants.SEARCH_SCREEN_HEADER + ( ( investors_clicked + 0.5 ) * constants.INVESTOR_HEIGHT ), True)

        crawl_portfolio()

        go_back()

        investors_clicked += 1

    scrolls = 1
    indent = constants.SEARCH_SCREEN_FIRST_INDENT

    processing = True
    while processing:

        investors_clicked = 0

        # click investors until last one has been reached
        while constants.SEARCH_BANNER_HEIGHT + indent + ( ( investors_clicked + 1 ) * constants.INVESTOR_HEIGHT ) < constants.SCREEN_HEIGHT:

            scroll(-scrolls, True)

            click_link(200, constants.SEARCH_BANNER_HEIGHT + indent + ( ( investors_clicked + 0.5 ) * constants.INVESTOR_HEIGHT ))

            crawl_portfolio()

            go_back()

            investors_clicked += 1

        scrolls += 1
            
        # calculate new indent of topmost stock
        relevant_bottom = constants.SCREEN_HEIGHT - ( constants.SCREEN_HEIGHT - ( constants.SEARCH_BANNER_HEIGHT + indent ) ) % constants.INVESTOR_HEIGHT
        indent = (relevant_bottom - constants.SEARCH_BANNER_HEIGHT ) - constants.SCROLL_CLICK_LENGTH



# Click at coordinates (x, y) and tag the current time
def click_link(x: int, y: int, pop=False): 

    print("Clicked at ["+str(x)+", "+str(y)+"]")

    pyautogui.click(x, y)

    process_html(pop)



# Scroll a <scrolls> number of time
def scroll(scrolls: int, infinite_scrolling_down=False):

    print("Scrolled "+str(scrolls)+" ticks")

    if infinite_scrolling_down:
        for i in range(-scrolls):
            pyautogui.scroll(-1)
            time.sleep(constants.INFINITE_SCROLL_WAIT)
    else:
        pyautogui.scroll(scrolls)

    time.sleep(constants.SCROLL_WAIT)



# Go back to the previous page
def go_back():

    print("Went back")

    with pyautogui.hold('alt'):
        pyautogui.press(['left'])
    
    process_html(True)



# Wait for and process a new html file
def process_html(pop=False):

    initial_html_files = set(pathlib.Path(constants.HTML_SAVE_DIR).glob("*.html"))

    while True:

        current_html_files = set(pathlib.Path(constants.HTML_SAVE_DIR).glob("*.html"))
        new_files = current_html_files - initial_html_files
        
        if new_files:
            # Return the first new file found
            new_file = next(iter(new_files))
            if pop:
                new_file.unlink()
            else:
                shutil.move(new_file, "./html_storage")
            break
        
        # Wait before checking again
        time.sleep(0.5)