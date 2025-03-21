from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mlbtime
import pandas

# Web driver and Beautiful Soup objects
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox") 
options.headless = True
wd = webdriver.Chrome("/usr/local/bin/chromedriver", options = options)
soup = BeautifulSoup()

# Scrapes the dates
def scrape_dates() -> list:
    global soup
    container_attr = 'ScheduleCollectionGridstyle__SectionLabelContainer-sc-c0iua4-4 fmyann'
    dates = [element.get_text(separator = ' ') for element in soup.find_all('div', class_ = container_attr)]
    return [mlbtime.yyyy_mm_dd(date) for date in dates]

# Scrapes the games
def scrape_games() -> list:
    global soup
    gameday_container_attr = 'ScheduleCollectionGridstyle__SectionWrapper-sc-c0iua4-0 guIOQi'
    game_container_attr = 'ScheduleGamestyle__DesktopScheduleGameWrapper-sc-b76vp3-0 bPxDLD'
    return [element.find_all('div', class_ = game_container_attr) for element in soup.find_all('div', class_ = gameday_container_attr)]

# Scrapes the game subjects
def scrape_subject(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    container_attr = 'TeamMatchupLayerstyle__TeamMatchupLayerWrapper-sc-ouprud-0 gQznxP teammatchup-teaminfo'
    subject_container = soup.find('div', class_ = container_attr)
    subject_list = subject_container.get_text(separator = ' ').split()[1:4]
    return ' '.join(subject_list)

# Scrapes the game times
def scrape_time(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    container_attr = 'linkstyle__AnchorElement-sc-1rt6me7-0 lcFuuA gameinfo-gamedaylink'
    return soup.find('a', class_ = container_attr).text

# Scrapes the game broadcast networks
def scrape_networks(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    container_attr = 'BroadcasterLayerstyle__BroadcasterLayerWrapper-sc-h8c8qu-0 gVCTUQ broadcaster-layer'
    return soup.find('div', class_ = container_attr).get_text()

# Scapes the schedule
def scrape() -> pandas.DataFrame:
    dates = scrape_dates()
    sdgames_html = scrape_games()
    df = pandas.DataFrame(columns = ['Subject', 'Date', 'Time', 'Networks'])
    for i, sdgames in enumerate(sdgames_html):
        for game in sdgames:
            subject = scrape_subject(str(game))
            date = dates[i]
            time = scrape_time(str(game))
            networks = scrape_networks(str(game))
            df = df.append({'Subject': subject, 'Date': date, 'Time': time, 'Networks': networks}, ignore_index = True)
    return df

# Scrapes the data mlb website
def read(url:str) -> pandas.DataFrame:
    global soup
    wd.get(url)
    soup = BeautifulSoup(wd.page_source, 'html.parser')
    return scrape()

# Driver
def main():
    url = input('Enter the MLB schedule url: ')
    soup = BeautifulSoup(wd.page_source, 'html.parser')
    df = read(url)
    folderpath = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/mlb/mlb-data/mlb-raw'
    startdate = input('Enter the schedule start date: ')
    enddate = input('Enter the schedule end date: ')
    filename = 'mlb-' + startdate + '-' + enddate + '-raw.csv'
    df.to_csv(folderpath + '/' + filename)

# Driver call
if __name__ == '__main__':
    main()