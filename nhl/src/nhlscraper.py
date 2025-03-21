from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import nhltime
import nhlcleaner
import pandas

# Webdriver and BeautifulSoup objects for web scraping
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox') 

# Webdriver and BeautifulSoup objects for web scraping
wd = webdriver.Chrome('/usr/local/bin/chromedriver', options = options)
url = 'https://www.nhl.com/schedule'
wd.get(url)
while str(wd.page_source) == '':
    wd.get(url)
soup = BeautifulSoup(wd.page_source, 'html.parser')

# Scrapes the game dates
def scrape_dates() -> list:
    global soup
    return [nhltime.convert_date(s.get_text()) for s in soup.find_all('div', class_ = 'section-subheader')]

# Scrapes the HTML tables containing game information
def scrape_tables() -> pandas.DataFrame:
    global soup
    dates = [nhltime.convert_date(s.get_text()) for s in soup.find_all('div', class_ = 'section-subheader')]
    tables = soup.find_all('table', class_ = 'day-table')
    for i in range(len(tables)):
        table = pandas.read_html(str(tables[i]))[0]
        table['Date'] = [dates[i]] * len(table)
        tables[i] = table
    return pandas.concat(tables)

# Cleans the resulting data frame
def clean_df(df:pandas.DataFrame) -> pandas.DataFrame:
    df.reset_index(drop = True, inplace = True)
    drop_list = [column for column in df.columns if 'Unnamed' in column]
    df.drop(drop_list, axis = 1, inplace = True)
    df = df.rename(columns={'Matchup Matchup':'Subject', 'Time Time':'Start Time', 'Networks Networks':'Network'})
    for i in range(len(df)):
        if 'TBD' not in str(df['Start Time'][i]):
            times = str(df['Start Time'][i]).split('ET ')
            df['Start Time'][i] = times[1]
    return df

# Driver
def main():
    # Scrape the NHL website for game information
    df = scrape_tables()
    df = clean_df(df)
    # Save the raw data frame to a CSV file
    folderpath = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/nhl/nhl-data/nhl-raw'
    startdate = input('Enter the schedule start date: ')
    enddate = input('Enter the schedule end date: ')
    filename = 'nhl-' + startdate + '-' + enddate + '-raw.csv'
    df.to_csv(folderpath + '/' + filename)
    # Clean the raw data frame and save it to a CSV file
    df = nhlcleaner.clean(df)
    folderpath = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/nhl/nhl-data/nhl-clean'
    filename = filename.replace('raw', 'clean')
    df.to_csv(folderpath + '/' + filename)

# Driver call
if __name__ == '__main__':
    main()
