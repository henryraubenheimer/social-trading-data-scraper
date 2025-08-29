from bs4 import BeautifulSoup, Comment

from datetime import datetime
import os
import re

import classes



# Process data files in html_storage one by one
def parse_files():

    os.makedirs('html_storage', exist_ok=True)
    for i in [1, 2]:
        for filename in os.listdir("html_storage/"):

            file_path = os.path.join("html_storage/", filename)
            with open(file_path) as fp:
                soup = BeautifulSoup(fp, features="html.parser")

            comment = soup.find(string=lambda text: isinstance(text, Comment))
            url = re.search(r'url:\s*(https?://[^\s]+)', comment).group(1).split('/')
            saved_date = datetime.strptime(re.search(r'[A-Za-z]{3} [A-Za-z]{3} \d{1,2} \d{4} \d{2}:\d{2}:\d{2}', comment).group(), '%a %b %d %Y %H:%M:%S')

            if i == 1:
                if url[3] == "discover":
                    parse_investors(soup, saved_date.date())
            else:
                print(url)
                if url[3] == "people" or url[3] == "smartportfolios":
                    if url[-1] == "portfolio":
                        parse_portfolio(soup, url[-2], saved_date.date())
                    else:
                        parse_share_transactions(soup, url[-3], url[-1].upper())



# Parse a portfolio page
def parse_portfolio(soup: BeautifulSoup, investor: str, date: datetime.date):

    # Find all the share positions
    share_positions = soup.find_all('div', {
        'automation-id': 'watchlist-grid-instruments-list',
        'class': 'et-table-row clickable-row ng-star-inserted'
    })

    share_list = []
    share_position_list = []
    # Extract info from these share positions
    for share_position in share_positions:

        share = share_position.find('div', {
            'automation-id': 'cd-public-portfolio-table-item-title',
            'class': 'et-font-xs et-bold-font ellipsis'
        }).text.strip()
        direction = share_position.find('div', {
            'class': 'et-font-weight-normal ng-star-inserted'
        }).text.strip()
        invested = share_position.find('div', {
            'class': 'et-font-weight-normal et-flex justify-end et-font-s ng-star-inserted'
        })
        invested = float(invested.text.replace(',', '').strip('<>% '))
        profit = share_position.find('div', {
            'class': 'et-font-weight-normal et-flex justify-end et-positive et-font-s ng-star-inserted'
        })
        if not profit: # If a loss was made
            profit = share_position.find('div', {
                'class': 'et-font-weight-normal et-flex justify-end et-negative et-font-s ng-star-inserted'
            })
        if not profit: # If no profit or loss was made
            profit = share_position.find('div', {
                'class': 'et-font-weight-normal et-flex justify-end et-font-s ng-star-inserted'
            })
        profit = float(profit.text.replace(',', '').strip('<>% '))
        value = share_position.find('div', {
            'class': 'et-font-weight-normal et-flex justify-end et-font-s ng-star-inserted'
        })
        value = float(value.text.replace(',', '').strip('<>% '))

        share_list.append({'ticker': share})
        share_position_list.append({'investor': investor, 'share': share, 'time': date, 'direction': direction, 'invested': invested, 'profit_loss': profit, 'value': value})

    classes.share.insert_many(share_list).on_conflict_ignore().execute()  
    classes.share_position.insert_many(share_position_list).on_conflict_ignore().execute()



# Parse a share transaction page
def parse_share_transactions(soup: BeautifulSoup, investor: str, share: str):

    # Find all the transactions
    transactions = soup.find_all('div', {
        'automation-id': 'watchlist-grid-instruments-list',
        'class': 'et-table-row ng-star-inserted'
    })

    share_list = []
    transaction_list = []
    # Extract info from these transactions
    for transaction in transactions:
        
        time = transaction.find('span', {
            'class': 'ng-star-inserted'
        }).text
        time = datetime.strptime(time, '%d/%m/%Y %H:%M')
        finds = transaction.find_all('span', { # for some reason amount an open are of the same class
            'class': 'et-font-weight-normal ets-num-s'
        })
        amount = finds[0]
        amount = float(amount.text.replace(',', '').strip('<>% '))
        leverage = transaction.find('span', {
            'class': 'et-font-weight-normal et-font-s ng-star-inserted'
        })
        leverage = float(leverage.text.replace('X', ''))
        open = finds[1]
        open = float(open.text.strip('<>% '))
        profit = transaction.find('span', {
            'class': 'et-font-weight-normal et-positive ets-num-s'
        })
        if not profit: # If a loss was made
            profit = transaction.find('span', {
                'class': 'et-font-weight-normal et-negative ets-num-s'
            })
        if not profit: # If no profit or loss was made
            profit = transaction.find('span', {
                'class': 'et-font-weight-normal ets-num-s'
            })
        profit = int(profit.text) 
        sl = transaction.find('span', {
            'class': 'et-font-weight-normal ets-num-s ng-star-inserted'
        })
        if not sl: # rarely theres no sl. Doing this as a temporary fix
            sl = 0.0001
        else:
            sl = float(sl.text)

        share_list.append({'ticker': share})
        transaction_list.append({'time': time, 'investor': investor, 'share': share, 'amount': amount, 'leverage': leverage, 'open': open, 'profit_loss': profit, 'sl': sl})

    classes.share.insert_many(share_list).on_conflict_ignore().execute()
    classes.transaction.insert_many(transaction_list).on_conflict_ignore().execute()



# Parse an investor search result list
def parse_investors(soup: BeautifulSoup, date: datetime.date):

    # Find all the investors
    investors = soup.find_all('div', {
        'automation-id': 'watchlist-grid-instruments-list',
        'class': 'et-table-row ng-star-inserted'
    })

    investor_list = []
    investor_data_list = []
    # Extract info from these investors
    for investor in investors:
        name = investor.find('div', {
            'automation-id': 'discover-people-results-list-item-nickname',
            'class': 'user-nickname'
        }).text.strip()
        profit = investor.find('span', {
            'automation-id': 'discover-people-results-list-item-gain',
            'class': 'positive'
        })
        if not profit:
            profit = investor.find('span', {
                'automation-id': 'discover-people-results-list-item-gain',
                'class': 'negative'
            })
        profit = float(profit.text.replace(',', '').strip('<>% '))
        risk_score = investor.find('span', {
            'automation-id': 'discover-people-results-list-item-risk-score'
        })
        risk_score = int(risk_score['class'][0][-1])
        copiers = int(investor.find('span', {
            'automation-id': 'discover-people-results-list-item-copiers-num'
        }).text.replace(',', ''))

        investor_list.append({'name': name})
        investor_data_list.append({'investor': name, 'time': date, 'profit': profit, 'risk': risk_score, 'copiers': copiers})

    classes.investor.insert_many(investor_list).on_conflict_ignore().execute()
    classes.investor_data.insert_many(investor_data_list).on_conflict_ignore().execute()