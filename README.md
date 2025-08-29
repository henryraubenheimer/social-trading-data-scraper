This repository holds code for scraping data (in a pretty unconventional way) from a social trading platform's website. This scraper is not general purpose and is hard coded for a specific platform which I'll keep anonymous to not contravene their company policy. The scraper works in two phases:

<ul>
  <li> A website navigator </li>
  <li> An html parser </li>
</ul>

The website navigator works by clicking through relevant pages on the website with an auto-clicker, and having an html extension download these pages automatically. This evades any anti-bot detection systems the website has, which easily pick up standard web scrapers like BeautifulSoup or Selenium.

### Set Up TODO

Manual tasks that need completing before starting:

<ul>
  <li> Investor button screenshot in search results (from right edge of portrait to right before scrollbar) saved as 'screenshots/investor.png' </li>
  <li> Share position button screenshot (from right edge of portrait to right before buy and sell data) saved as 'screenshots/share position.png' </li>
  <li> Unclicked 'Portfolio' button screenshot found in the investor portfolio page saved as 'screenshots/portfolio button.png' </li>
</ul>
