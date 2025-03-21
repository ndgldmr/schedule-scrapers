from bs4 import BeautifulSoup
import requests
import pga_time
import pandas

# Scrapes the event schedule for given dates
def scrape() -> pandas.DataFrame:
    # BeautifulSoup object and list of data frames from webpage HTML tables
    url = 'https://www.sportsmediawatch.com/pga-tour-tv-schedule-2023-cbs-nbc-golf-channel-espn-plus/'
    webpage = requests.get(url)
    html = webpage.text
    soup = BeautifulSoup(webpage.content, 'html.parser')
    dfs = pandas.read_html(html)
    # List of dates, each corresponding to a data frame in dfs
    dates = [pga_time.format_date(date.get_text()) for date in soup.find_all('span', class_ = 'bold')[:-2] if 'Featured Groups' not in date.get_text()]
    # If there are an equal amount of data frames and dates
    if len(dfs) == len(dates):
        # Add a date column to each data frame in dfs
        for i in range(len(dfs)):
            dfs[i]['Date'] = [dates[i]] * len(dfs[i])
        # Form the event data frame using the user-inputted list of event dates
        event_dates = input('Enter the event dates in YYYY-MM-DD form, each separted by a single comma: ').split(',')
        event_dfs = list()
        for df in dfs:
            if df['Date'][0] in event_dates:
                event_dfs.append(df)
        event_df = pandas.concat(event_dfs)
        # Reset the event_df and sort the values according to date
        event_df.sort_values('Date', inplace = True)
        event_df.reset_index(drop = True, inplace = True)
        # Return the event_df
        return event_df

# Converts the start/end date-times from EST to UTC  
def clean_times(df:pandas.DataFrame) -> pandas.DataFrame:
    # Convert each Start time and End time to it's corresponding HH:MM AM/PM format
    df['Start'] = df['Start'].apply(lambda text: text[:-1] + 'PM' if text.endswith('p') else (text[:-2] + 'AM' if text.endswith('am') else text))
    df['End'] = df['End'].apply(lambda text: text[:-1] + 'PM' if text.endswith('p') else (text[:-2] + 'AM' if text.endswith('am') else text))
    # Convert each start time and end time to it's corresponding 24-hour time in HH:MM:SS format
    df['Start'] = df['Start'].apply(pga_time.time24hour)
    df['End'] = df['End'].apply(pga_time.time24hour)
    # Convert each start time and end time to it's corresponding date time
    for i in range(len(df)):
        df['Start'][i] = str(df['Date'][i]) + ' ' + str(df['Start'][i])
        df['End'][i] = str(df['Date'][i]) + ' ' + str(df['End'][i])
    df['Start'] = df['Start'].apply(pga_time.est_to_utc)
    df['End'] = df['End'].apply(pga_time.est_to_utc)
    # Return the df
    return df

# Adds a channel id column to each row
def clean_tv(df:pandas.DataFrame) -> pandas.DataFrame:
    # Make new rows for each row with more than one TV value
    df['TV'] = df['TV'].str.split(', ')
    df = df.explode('TV')
    df = df.reset_index(drop = True)
    # Add a channel id column for each row
    for i in range(len(df)):
        file = open('/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/pga/pga-data/pga-channels.txt', 'r')
        for line in file:
            key, value = line.rstrip().split(',')
            if df['TV'][i] ==  key:
                df.at[i, 'Channel ID'] = value
                break
    # Make new row for NBC Channel ID
    df2 = df.copy(deep = True)
    for i in range(len(df2)):
        if df2['TV'][i] == 'NBC':
            df2['Channel ID'][i] = 'GOLF(GOLF)-1635'
    df = df.append(df2)
    df.sort_values(['Date', 'Start'], inplace = True)
    df = df.drop_duplicates()
    df.reset_index(drop = True, inplace = True)
    # Return the df
    return df

# Adds a sport, home team, and away team column
def clean_sportteams(df:pandas.DataFrame) -> pandas.DataFrame:
    # Add home team, away team, and sport columns
    df['Sport'] = ['Golf'] * len(df)
    df['Home Team'] = ['Golf'] * len(df)
    df['Away Team'] = ['Golf'] * len(df)
    # Return the df
    return df

# Reorders the data frame columns
def reorder_columns(df:pandas.DataFrame) -> pandas.DataFrame:
    # Reorder columns
    new_order = ['Round', 'Date', 'TV', 'Channel ID', 'Start', 'End', 'Sport', 'Home Team', 'Away Team']
    df = df.reindex(columns = new_order)
    # Return the data frame
    return df

# Driver
def main():
    df = scrape()
    df = clean_times(df)
    df = clean_tv(df)
    df = clean_sportteams(df)
    df = reorder_columns(df)
    df.to_csv(input('Enter the event name: ') + '.csv')

# Driver call
if __name__ == '__main__':
    main()