from bs4 import BeautifulSoup
import pyautogui
import pyscreeze

import pathlib
import shutil
import time

import constants



# crawl the page detailing purchases for a specific share by a specific investor
def crawl_share():
    pass



# crawl the page detailing the portfolio for a specific investor
def crawl_portfolio():

    scrolls = 0

    # Find and click the portfolio button screen
    portfolio_button = pyautogui.locateOnScreen('screenshots/portfolio button.png', grayscale=True)
    center = pyautogui.center(portfolio_button)
    click_link(center.x, center.y)

    relevant_top = 0 # the ceiling of the first relevant stock position
    while True:

        try:
            # find all sections on the screen that look like share positions
            unfiltered_boxes = pyautogui.locateAllOnScreen('screenshots/share position.png', region=(0, relevant_top, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT-relevant_top), grayscale=True, confidence=constants.SHARE_POSITION_MATCH_CONFIDENCE)
            unfiltered_boxes = list(unfiltered_boxes)
            share_positions = filter_overlapping_boxes(unfiltered_boxes)
        except pyscreeze.ImageNotFoundException: # If no new shares have been found, break
            break

        # calculate the mean share height
        mean_height = 0
        for share_position in share_positions:
            mean_height += share_position.height
        mean_height /= len(share_positions)   

        # click through the shares
        for share_position in share_positions:

            center = pyautogui.center(share_position)
            click_link(center.x, center.y)

            go_back(True)

            scroll(-scrolls)

        scrolls += 1
        scroll(-1)

        relevant_top = share_positions[-1].top + share_position.height - constants.SCROLL_DISTANCE

    go_back()



# crawl the page listing investor search results
def crawl_search():

    scrolls = 0

    while True:

        # find all sections on the screen that look like investor buttons
        unfiltered_boxes = pyautogui.locateAllOnScreen('screenshots/investor.png', grayscale=True, confidence=constants.INVESTOR_MATCH_CONFIDENCE)
        unfiltered_boxes = list(unfiltered_boxes)
        investors = filter_overlapping_boxes(unfiltered_boxes)

        for investor in investors:

            center = pyautogui.center(investor)
            click_link(investor.left, center.y)

            crawl_portfolio()

            go_back(True)

            scroll(-scrolls, True)

        scrolls += ((unfiltered_boxes[-1].top + unfiltered_boxes[-1].height) - unfiltered_boxes[0].top) // constants.SCROLL_DISTANCE
        scroll(-((unfiltered_boxes[-1].top + unfiltered_boxes[-1].height) - unfiltered_boxes[0].top) // constants.SCROLL_DISTANCE, True)



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
            pyautogui.scroll(-1, x=constants.SCROLL_X, y=constants.SCROLL_Y)
            time.sleep(constants.INFINITE_SCROLL_WAIT)
    else:
        pyautogui.scroll(scrolls, x=constants.SCROLL_X, y=constants.SCROLL_Y)

    time.sleep(constants.SCROLL_WAIT)



# Go back to the previous page
def go_back(pop=True):

    print("Went back")

    with pyautogui.hold('alt'):
        pyautogui.press(['left'])
    
    process_html(pop)



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
                # Remove data intensive style tags
                soup = BeautifulSoup(new_file.read_text(encoding='utf-8'), features="html.parser")
                for style_tag in soup.find_all('style'):
                    style_tag.decompose()
                new_file.write_text(str(soup), encoding='utf-8')

                shutil.move(new_file, "./html_storage")
            break
        
        # Wait before checking again
        time.sleep(0.5)



# Given a list of located investor / share position bounding boxes, find distinct boxes
def filter_overlapping_boxes(boxes):
    
    # Sort boxes by area (largest first) to prioritize keeping larger matches
    boxes_with_area = [(box, box[2] * box[3]) for box in boxes]
    boxes_with_area.sort(key=lambda x: x[1], reverse=True)
    
    filtered_boxes = []
    
    for current_box, _ in boxes_with_area:
        left1, top1, width1, height1 = current_box
        right1 = left1 + width1
        bottom1 = top1 + height1
        area1 = width1 * height1
        
        # Check if this box overlaps significantly with any already accepted box
        should_keep = True
        
        for existing_box in filtered_boxes:
            left2, top2, width2, height2 = existing_box
            right2 = left2 + width2
            bottom2 = top2 + height2
            area2 = width2 * height2
            
            # Calculate intersection
            intersect_left = max(left1, left2)
            intersect_top = max(top1, top2)
            intersect_right = min(right1, right2)
            intersect_bottom = min(bottom1, bottom2)
            
            # Check if there's actual intersection
            if intersect_left < intersect_right and intersect_top < intersect_bottom:
                intersect_area = (intersect_right - intersect_left) * (intersect_bottom - intersect_top)
                
                # Calculate overlap ratio relative to the smaller box
                smaller_area = min(area1, area2)
                overlap_ratio = intersect_area / smaller_area
                
                # If overlap exceeds threshold, don't keep this box
                if overlap_ratio > constants.MIN_BUTTON_OVERLAP:
                    should_keep = False
                    break
        
        if should_keep:
            filtered_boxes.append(current_box)
    
    return filtered_boxes