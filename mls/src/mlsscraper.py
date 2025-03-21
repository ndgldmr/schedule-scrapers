from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mlscleaner
import pandas

# Webdriver options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox') 
options.headless = True

# Webdriver and Beautiful Soup objects for web scraping
wd = webdriver.Chrome('/usr/local/bin/chromedriver', options = options)
url = input('Enter the schedule url: ')
wd.get(url)
while str(wd.page_source) == '':
    wd.get(url)
soup = BeautifulSoup(wd.page_source, 'html.parser')

# Scrapes the game HTML
def scrape_games() -> pandas.DataFrame:
    global soup
    # Scrape HTML for game information
    game_html = soup.find_all('div', class_ = 'sc-iOeugr jzQVmO mls-c-match-list__match')
    dates, times, home_teams, away_teams, channels = list(), list(), list(), list(), list()
    for html in game_html:
        soup_html = BeautifulSoup(str(html), 'html.parser')
        dates.append(soup_html.find('div', class_ = 'sc-iveFHk jsryXz mls-c-status-stamp__status -pre').get_text())
        times.append(soup_html.find('div', class_ = 'sc-iBYQkv kSdEbl').get_text())
        home_teams.append(soup_html.find_all('span', class_ = 'mls-c-club__shortname')[0].get_text())
        away_teams.append(soup_html.find_all('span', class_ = 'mls-c-club__shortname')[1].get_text())
        channels.append(soup_html.find('span', class_ = 'sc-bjfHbI dPLjhg').get_text())
    # Construct data frame with the scraped information
    data = {'Date':dates, 'Time':times, 'Home Team':home_teams, 'Away Team':away_teams, 'Channel':channels}
    return pandas.DataFrame(data)

# Driver
def main():
    # Scrape the schedule information
    df = scrape_games()
    # Save the raw data frame to a CSV file
    folderpath = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/mls/mls-data/mls-raw'
    startdate = input('Enter the schedule start date: ')
    enddate = input('Enter the schedule end date: ')
    filename = 'mls-' + startdate + '-' + enddate + '-raw.csv'
    df.to_csv(folderpath + '/' + filename)
    # Clean the raw data frame and save it to a CSV file
    df = mlscleaner.clean(df)
    folderpath = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/mls/mls-data/mls-clean'
    filename = filename.replace('raw', 'clean')
    df.to_csv(folderpath + '/' + filename)

# Driver call
if __name__ == '__main__':
    main()