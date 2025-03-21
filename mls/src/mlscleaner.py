import mlstime
import pandas

# Cleans the team columns
def clean_teams(df:pandas.DataFrame):
    # Upload the MLS team name data
    file = open('/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/mls/mls-data/mls-text-files/mls-teams.txt', 'r')
    teams = {line.split(',')[0]:line.strip().split(',')[1] for line in file}
    # Clean the team names
    for i in range(len(df)):
        df['Home Team'][i] = teams[df['Home Team'][i]]
        df['Away Team'][i] = teams[df['Away Team'][i]]
        df.at[i, 'Subject'] = df['Home Team'][i] + ' vs. ' + df['Away Team'][i]
        df.at[i, 'Sport'] = 'Soccer'

# Cleans the channel column and adds a channel id column
def clean_channels(df:pandas.DataFrame) -> pandas.DataFrame:
    # Make new rows for games broadcasting on multiple channels
    df['Channel'] = df['Channel'].str.split(', ')
    df = df.explode('Channel')
    df = df.reset_index(drop = True)
    # Add a channel ID column to each row
    file = open('/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/mls/mls-data/mls-text-files/mls-channels.txt', 'r')
    channels = {line.split(',')[0]:line.strip().split(',')[1] for line in file}
    for i in range(len(df)):
        df.at[i, 'Channel ID'] = channels[df['Channel'][i]]
    return df

# Cleans the start/end date-times
def clean_datetimes(df:pandas.DataFrame) -> pandas.DataFrame:
    # Convert the date and time formats
    df['Date'] = df['Date'].apply(mlstime.convert_date)
    df['Time'] = df['Time'].apply(mlstime.time24hour)
    df = df.rename(columns = {'Time': 'Start Time'})
    # Change the start time format
    for i in range(len(df)):
        df['Start Time'][i] = df['Date'][i] + ' ' + df['Start Time'][i]
    # Subtract 30 minutes from the start time, and add 210 minutes to the result to get the end time
    df['Start Time'] = df['Start Time'].apply(mlstime.subtract30minutes)
    df['End Time'] = df['Start Time'].apply(mlstime.add210minutes)
    # Convert the start/end date-times from ET to UTC
    df['Start Time'] = df['Start Time'].apply(mlstime.utc)
    df['End Time'] = df['End Time'].apply(mlstime.utc)
    # Return the data frame
    return df

# Cleans the MLS data frame schedule
def clean(df:pandas.DataFrame) -> pandas.DataFrame:
    clean_teams(df)
    df = clean_channels(df)
    df = clean_datetimes(df)
    return df