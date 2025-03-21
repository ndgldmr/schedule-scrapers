from bs4 import BeautifulSoup
from lpgatime import *
import requests
import pandas

# Scrapes the LPGA match information
def scrape() -> pandas.DataFrame:
    # BeautifulSoup object for web scraping
    url = input('Enter a tournement url from the website https://www.lpga.com/tournaments: ')
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    html = webpage.text

    # List of tournement info
    info = [i.get_text() for i in soup.find_all('span', class_ = 'slotinfo')]
    for i in range(len(info)):
        if '(ET)' in info[i]:
            info[i] = info[i].replace('(ET)', '')
        elif '(Stream ET)' in info[i]:
            info[i] = info[i].replace('(Stream ET)', '')
        elif '(Tape ET)' in info[i]:
            info[i] = info[i].replace('(Tape ET)', '')

    # List of tournement dates
    dates = []
    for s in info:
        if s.split()[0] in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
            dates.append(s.split()[0] + ' ' + s.split()[1])

    # Clean the tournement dates
    for i in range(len(dates)):
        dates[i] = dates[i] + ' 2023'
        date_obj = datetime.datetime.strptime(dates[i], '%B %d %Y')
        dates[i] = date_obj.strftime('%Y-%m-%d')

    # List of tournement channels
    channels = []
    for i in range(len(info)):
        if 'Golf Channel' in info[i]:
            channels.append('Golf Channel')
        elif 'NBC' in info[i]:
            channels.append('NBC')
        elif 'Peacock' in info[i]:
            channels.append('Peacock')
        elif 'CBS' in info[i]:
            channels.append('CBS')

    # List of tournement start/end date-times
    start = []
    end = []
    for i in range(len(info)):
        if i % 2 != 0:
            start_time, end_time = info[i].split(' - ')
            start.append(convert_time(start_time + ' p.m.'))
            end.append(convert_time(end_time))
    for i in range(len(dates)):
        start[i] = est_to_utc(dates[i] + ' ' + start[i])
        end[i] = est_to_utc(dates[i] + ' ' + end[i])

    # Tournement data frame
    subject = [input('Enter the tournement name: ')] * len(start)
    data = {'Subject' : subject, 'Date' : dates, 'Broadcast' : channels, 'Start Time (UTC)' : start, 'End Time (UTC)' : end}
    df = pandas.DataFrame(data)
    df['Sport'] = ['Golf'] * len(df)
    df['Home Team'] = ['Golf'] * len(df)
    df['Away Team'] = ['Golf'] * len(df)
    
    # Add a channel id column to each row
    for i in range(0, len(df)):
        if df.loc[i, 'Broadcast'] == 'CBS':
            df.loc[i, 'Channel ID'] = 'WCBS(CBS)-8008'
        elif df.loc[i, 'Broadcast'] == 'Golf Channel':
            df.loc[i, 'Channel ID'] = 'GOLF(GOLF)-1635'
        elif df.loc[i, 'Broadcast'] == 'NBC':
            df.loc[i, 'Channel ID'] = 'GOLF(GOLF)-1635' 
        elif df.loc[i, 'Broadcast'] == 'Peacock':
            df.loc[i, 'Channel ID'] = 'Peacock'
    
    # Make a duplicate row for NBC
    df2 = df.copy(deep = True)
    for i in range(len(df2)):
        if df2['Broadcast'][i] == 'NBC':
            df2['Channel ID'][i] = 'WNBC(NBC)-8009'
    df = df.append(df2)
    df.sort_values(['Date', 'Start Time (UTC)'], inplace = True)
    df = df.drop_duplicates()
    df.reset_index(drop = True, inplace = True)

    # Reorder the data frame columns 
    new_order = ['Subject', 'Date', 'Broadcast', 'Channel ID', 'Start Time (UTC)', 'End Time (UTC)', 'Sport', 'Home Team', 'Away Team']
    df = df.reindex(columns = new_order)

    # Return the data frame 
    return df
    
# Driver
def main():
    df = scrape()
    df.to_csv(input('Enter a file name ending in .csv to save the schedule: '))

# Driver call
if __name__ == '__main__':
    main()