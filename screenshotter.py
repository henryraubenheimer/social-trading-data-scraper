import pyautogui
import time

# Constants (in pixels)
INVESTOR_BANNER_HEIGHT = 250
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCROLL_CLICK_LENGTH = 138
SHARE_HEIGHT = 58

time.sleep(5)

counter = 0
scrolls = 2 # how many times there has been scrolled
scroll_indent = 0 # how far the topmost stock is from the top

while True:

    shares_clicked = 0 # how many shares on the current screen have been clicked

    while INVESTOR_BANNER_HEIGHT + scroll_indent + ( ( shares_clicked + 1) * SHARE_HEIGHT ) < SCREEN_HEIGHT:

        pyautogui.scroll(-scrolls)

        time.sleep(1)

        # click stock
        if not pyautogui.pixelMatchesColor(200, INVESTOR_BANNER_HEIGHT + scroll_indent + ( ( shares_clicked + 0.5 ) * SHARE_HEIGHT ), (255, 255, 255)):
            break
        pyautogui.click(200, INVESTOR_BANNER_HEIGHT + scroll_indent + ( ( shares_clicked + 0.5 ) * SHARE_HEIGHT ))
        counter += 1
        #print(INVESTOR_BANNER_HEIGHT + scroll_indent + ( ( shares_clicked + 0.5 ) * SHARE_HEIGHT ))

        time.sleep(3)

        pyautogui.scroll(-2)

        time.sleep(1)

        pyautogui.screenshot('screenshots/screenshot_'+str(counter)+'.png')

        # go back to portfolio page
        with pyautogui.hold('alt'):
            pyautogui.press(['left'])

        time.sleep(2)

        shares_clicked += 1

    # check if the end has been reached
    try:
        pyautogui.locateOnScreen('bottom_indicator.png', confidence=0.8)
        print("Finished!")
        break

    # scroll to new shares
    except pyautogui.PyAutoGUIException:
        
        relevant_bottom = SCREEN_HEIGHT - ( SCREEN_HEIGHT - ( INVESTOR_BANNER_HEIGHT + scroll_indent ) ) % SHARE_HEIGHT
        new_scrolls = ( relevant_bottom - INVESTOR_BANNER_HEIGHT ) // SCROLL_CLICK_LENGTH
        scroll_indent = (relevant_bottom - INVESTOR_BANNER_HEIGHT ) - ( new_scrolls * SCROLL_CLICK_LENGTH )
        
        pyautogui.scroll(scrolls)
        scrolls += new_scrolls
    
    time.sleep(2)