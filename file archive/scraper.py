from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://www.etoro.com/people/noimportan3/portfolio/crox"

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
# Wait for AngularJS to be defined
wait = WebDriverWait(driver, 30)
wait.until(lambda driver: driver.execute_script("return typeof angular !== 'undefined'"))
# Wait for AngularJS to bootstrap
wait.until(lambda driver: driver.execute_script(
    "return angular.element(document.body).injector() != null"
))
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")

output = soup.find_all("span", class_="ng-star-inserted")
