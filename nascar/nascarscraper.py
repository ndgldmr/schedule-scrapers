from bs4 import BeautifulSoup
import requests
import pandas
from nascartime import *

# Get the HTML code from the specified url
url = 'https://www.espn.com/racing/schedule'
page = requests.get(url)
html = page.text
soup = BeautifulSoup(page.content, 'html.parser')

# Rename the data frame columns
df = pandas.read_html(html)[0]
df = df.rename(columns={0: 'Date', 1: 'Subject', 2: 'Network', 3: 'Delete'})
df.drop('Delete', axis=1, inplace=True)
df.drop([0, 1, 33, 34], inplace=True)
df.reset_index(drop=True, inplace=True)

# Process dates and times
for i in range(len(df)):
    # Get the date and time
    date, time = split_date_time(df['Date'][i])
    df['Date'][i] = date
    df.at[i, 'Start Time (UTC)'] = date + ' ' + time
    df.at[i, 'End Time (UTC)'] = add3hours(df.at[i, 'Start Time (UTC)'])
df['Start Time (UTC)'] = df['Start Time (UTC)'].apply(utc)
df['End Time (UTC)'] = df['End Time (UTC)'].apply(utc)

# Add channel ids
for i in range(len(df)):
    if df['Network'][i] == 'FS1':
        df.at[i, 'Channel ID'] = 'FS1(Fox Sports 1)-9959'
    elif df['Network'][i] == 'USA Net':
        df.at[i, 'Channel ID'] = 'USA(USA)-968'
    elif df['Network'][i] == 'FOX':
        df.at[i, 'Channel ID'] = 'KTTV(Fox)-8024, WNYW(Fox)-8354'
    elif df['Network'][i] == 'NBC':
        df.at[i, 'Channel ID'] = 'KNBC(NBC)-8022, WNBC(NBC)-8009'

df['Channel ID'] = df['Channel ID'].str.split(', ')
df = df.explode('Channel ID')
df = df.reset_index(drop=True)

# Add the sport and home/away teams
for i in range(len(df)):
    df.at[i, 'Sport'] = 'Nascar'
    df.at[i, 'Home Team'] = 'Nascar'
    df.at[i, 'Away Team'] = 'Nascar'

# Reorder the data frame columns
order = ['Subject', 'Date', 'Network', 'Channel ID', 'Start Time (UTC)', 'End Time (UTC)', 'Sport', 'Home Team', 'Away Team']
df = df.reindex(columns= order)

# Save the data frame
df.to_csv('nascar-cup-series.csv')