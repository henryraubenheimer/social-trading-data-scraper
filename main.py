import constants
import crawlers
import data_extractors
import time

time.sleep(constants.INIT_WAIT)
extractor = data_extractors.extractor()
crawlers.crawl_portfolio(extractor)
#crawlers.crawl_search(extractor)