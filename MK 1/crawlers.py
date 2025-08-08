from datetime import datetime
from bs4 import BeautifulSoup
import pathlib
import peewee
import pyautogui
import time
import uuid

import classes
import constants

# crawl the page detailing purchases for a specific share by a specific investor
def crawl_share():

    # save the html
    with pyautogui.hold('ctrl'):
        pyautogui.press(['s']) # save
    time.sleep(constants.POPUP_WAIT)
    pyautogui.write('share') # name file
    time.sleep(constants.POPUP_WAIT)
    pyautogui.press(['enter']) # enter save
    time.sleep(constants.POPUP_WAIT)
    pyautogui.press(['enter']) # overwrite
    time.sleep(constants.DOWNLOAD_WAIT)
    pyautogui.click(200, 200)

    # parse the share html
    with open(pathlib.Path.home() / constants.HTML_SAVE_DIR / "share.html") as fp:
        soup = BeautifulSoup(fp, features="html.parser")
    # process all the investor data
    investor_name = soup.find('span', {
        'automation-id': 'user-header-full-name'
    })
    investors = classes.investor.filter(classes.investor.name == investor_name.text).execute() # TODO: refine this search
    share_name = soup.find('p', {
        'automation-id': 'cd-public-portfolio-breakdown-header-name'
    }).text
    buys = soup.find_all('div', {
        'automation-id': 'watchlist-grid-instruments-list'
    })
    print(investors)
    for buy in buys:
        for investor in investors:
            buy_time = buy.find('span', {
                'class': "ng-star-inserted"
            }).text
            classes.transaction.insert(id = uuid.uuid4(), time=datetime.strptime(buy_time, '%d/%m/%Y %H:%M'), investor_id=investor.id, share=share_name).execute()
            print(investor.name+' '+share_name+' transaction inserted')

# crawl the page detailing the portfolio for a specific investor
def crawl_portfolio():

    pyautogui.click(740, 360)
    time.sleep(constants.LOAD_PAGE_WAIT)

    # save the html
    with pyautogui.hold('ctrl'):
        pyautogui.press(['s']) # save
    time.sleep(constants.POPUP_WAIT)
    pyautogui.write('portfolio') # name file
    time.sleep(constants.POPUP_WAIT)
    pyautogui.press(['enter']) # enter save
    time.sleep(constants.POPUP_WAIT)
    pyautogui.press(['enter']) # overwrite
    time.sleep(constants.DOWNLOAD_WAIT)
    pyautogui.click(200, 200)

    # parse the portfolio html
    with open(pathlib.Path.home() / constants.HTML_SAVE_DIR / "portfolio.html") as fp:
        soup = BeautifulSoup(fp, features="html.parser")
    # process all the investor data
    investor_name = soup.find('span', {
        'automation-id': 'user-header-full-name'
    })
    investor_id = uuid.uuid4()
    classes.investor.insert(id=investor_id, name=investor_name.text).execute()
    print(investor_name.text+' investor inserted')
    # process all the share data in the portfolio
    shares = soup.find_all('div', {
        'automation-id': 'cd-public-portfolio-table-item-title',
        'class': 'et-font-xs et-bold-font ellipsis'
    })
    for share in shares:
        share = share.text.strip()
        try:
            classes.share.insert(ticker=share).execute()
            print(share+' share inserted')
        except peewee.IntegrityError:
            print(share+' already in database')
        classes.share_position.insert(id=uuid.uuid4(), investor_id=investor_id, share_id=share).execute()
    
    scrolls = 2 # how many times there has been scrolled
    indent = 0 # how far the topmost relevant stock is from the top

    processing = True
    while processing:

        shares_clicked = 0 # how many shares on the current screen have been clicked

        # click shares until last one has been reached
        while constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 1 ) * constants.SHARE_HEIGHT ) < constants.SCREEN_HEIGHT:

            pyautogui.scroll(-scrolls)
            time.sleep(constants.SCROLL_WAIT)

            # click stock
            if not pyautogui.pixelMatchesColor(200, constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 0.5 ) * constants.SHARE_HEIGHT ), (255, 255, 255)):
                processing = False
                break
            pyautogui.click(200, constants.INVESTOR_BANNER_HEIGHT + indent + ( ( shares_clicked + 0.5 ) * constants.SHARE_HEIGHT ))
            time.sleep(constants.LOAD_PAGE_WAIT)

            crawl_share()

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

    with pyautogui.hold('alt'):
        pyautogui.press(['left'])
    time.sleep(constants.LOAD_PAGE_WAIT)

    with pyautogui.hold('alt'):
        pyautogui.press(['left'])
    time.sleep(constants.LOAD_PAGE_WAIT)

# crawl the page listing investor search results
def crawl_search():

    # save the html
    with pyautogui.hold('ctrl'):
        pyautogui.press(['s']) # save
    time.sleep(constants.POPUP_WAIT)
    pyautogui.write('search') # name file
    time.sleep(constants.POPUP_WAIT)
    pyautogui.press(['enter']) # enter save
    time.sleep(constants.POPUP_WAIT)
    pyautogui.press(['enter']) # overwrite
    time.sleep(constants.DOWNLOAD_WAIT)
    pyautogui.click(150, 150)

    investors_clicked = 3
    investor_number = 3

    # click investors until last one has been reached before scrolling
    while constants.SEARCH_SCREEN_HEADER + ( ( investors_clicked + 1 ) * constants.INVESTOR_HEIGHT ) < constants.SCREEN_HEIGHT:

        pyautogui.click(200, constants.SEARCH_SCREEN_HEADER + ( ( investors_clicked + 0.5 ) * constants.INVESTOR_HEIGHT ))
        time.sleep(constants.LOAD_PAGE_WAIT)

        crawl_portfolio()

        # go back to search page
        with pyautogui.hold('alt'):
            pyautogui.press(['left'])
        time.sleep(constants.LOAD_PAGE_WAIT)

        investors_clicked += 1
        investor_number += 1

    scrolls = 1
    indent = constants.SEARCH_SCREEN_FIRST_INDENT

    processing = True
    while processing:

        investors_clicked = 0

        # click investors until last one has been reached
        while constants.SEARCH_BANNER_HEIGHT + indent + ( ( investors_clicked + 1 ) * constants.INVESTOR_HEIGHT ) < constants.SCREEN_HEIGHT:

            pyautogui.scroll(-scrolls)
            time.sleep(constants.SCROLL_WAIT)

            pyautogui.click(200, constants.SEARCH_BANNER_HEIGHT + indent + ( ( investors_clicked + 0.5 ) * constants.INVESTOR_HEIGHT ))
            time.sleep(constants.LOAD_PAGE_WAIT)

            crawl_portfolio()

            # go back to portfolio page
            with pyautogui.hold('alt'):
                pyautogui.press(['left'])
            time.sleep(constants.LOAD_PAGE_WAIT)

            investors_clicked += 1
            investor_number

        scrolls += 1
            
        # calculate new indent of topmost stock
        relevant_bottom = constants.SCREEN_HEIGHT - ( constants.SCREEN_HEIGHT - ( constants.SEARCH_BANNER_HEIGHT + indent ) ) % constants.INVESTOR_HEIGHT
        indent = (relevant_bottom - constants.SEARCH_BANNER_HEIGHT ) - constants.SCROLL_CLICK_LENGTH