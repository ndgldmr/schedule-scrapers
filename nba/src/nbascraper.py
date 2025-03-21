from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from nbagame import *
from nbatime import *
import pandas

# Webdriver options 
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox') 
options.headless = True

# Chrome webdriver and BeautifulSoup object
wd = webdriver.Chrome('/usr/local/bin/chromedriver', options = options)
wd.get('https://www.nba.com/schedule')
soup = BeautifulSoup(wd.page_source, 'html.parser')

# Driver
def main():
    # Global varaible used to scraping
    global soup
    # HTML code for each NBA gameday in the week. Each element of gamedayHTML will be scraped for it's date and list of NBA game HTML
    gamedayHTML = soup.find_all('div', class_ = 'ScheduleDay_sd__GFE_w') 
    gamedates = [format_date(dayHTML.find('h4', class_ = 'ScheduleDay_sdDay__3s2Xt').get_text()) for dayHTML in gamedayHTML]
    gamehtml = [day.find_all('div', class_ = 'ScheduleGame_sg__RmD9I') for day in gamedayHTML]
    # A dictionary from a date in YYYY-MM-DD format to a list of NBA games on that date in HTML form, and a list of NBA game objects.
    nbaday = {date : games for date, games in zip(gamedates, gamehtml)}
    nbagames = []
    # Construct the NBA game objects, construct a data frame from them, and save the data frame to a CSV file. 
    for key in nbaday:
        for value in nbaday[key]:
            nbagames.append(NbaGame(key, str(value)))
    df = pandas.DataFrame([{'Subject' : game.subject, 'Date' : game.date, 'Time' : game.time, 'Networks' : game.networks, 'Location' : game.location} for game in nbagames])
    # Save the data frame to a CSV file
    folderpath = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/nba/nba-data/raw-nba-data'
    startdate = input('Enter the schedule start date: ')
    enddate = input('Enter the schedule end date: ')
    filename = 'nba-' + startdate + '-' + enddate + '-raw.csv'
    df.to_csv(folderpath + '/' + filename)

# Driver call
if __name__ == '__main__':
    main()