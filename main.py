import constants
import crawlers
import re
import time

# time.sleep(constants.INIT_WAIT)
# crawlers.crawl_search()

# from bs4 import BeautifulSoup, Comment
# import pathlib
# # parse the share html
# with open("html_storage/8_8_2025 2：59：48 PM.html") as fp:
#     soup = BeautifulSoup(fp, features="html.parser")

# comment = soup.find(string=lambda text: isinstance(text, Comment))
# url = re.search(r'url:\s*(https?://[^\s]+)', comment).group(1)

# print(url[-9:])

import parsers
parsers.parse_files()
    # # Use regex to extract URL
    # url_match = re.search(r'url:\s*(https?://[^\s]+)', comment)
    # if url_match:
    #     url = url_match.group(1)
    #     print(f"Method 1 - Found URL: {url}")