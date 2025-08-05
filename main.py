import classes
import constants
import crawlers
from datetime import datetime
import time

from bs4 import BeautifulSoup
import peewee

classes.db.connect()
time.sleep(constants.INIT_WAIT)
crawlers.crawl_search()
