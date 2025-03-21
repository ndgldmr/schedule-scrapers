import pandas
import nhltime

# Cleans the subject column
def clean_subject(df:pandas.DataFrame) -> pandas.DataFrame:
    for i in range(len(df)):
        teams = df['Subject'][i].split(' @ ')
        teams[1] = teams[1][:-2]
        path = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/nhl/nhl-data/nhl-text-files/nhl-teams.txt'
        file = open(path, 'r')
        for line in file:
            teams[0] = line.rstrip() if teams[0] in line else teams[0]
            teams[1] = line.rstrip() if teams[1] in line else teams[1]
            if 'NY' in teams[0]:
                teams[0] = teams[0].replace('NY', 'New York')
            if 'NY' in teams[1]:
                teams[1] = teams[1].replace('NY', 'New York')
        df['Subject'][i] = teams[0] + ' at ' + teams[1]
        df.at[i, 'Away Team'] = teams[0]
        df.at[i, 'Home Team'] = teams[1]
    return df

# Cleans the start/end date-time columns
def clean_times(df:pandas.DataFrame) -> pandas.DataFrame:
    for i in range(len(df)):
        df['Start Time'][i] = nhltime.time24hour(df['Start Time'][i][:-3])
        start = df['Date'][i] + ' ' + df['Start Time'][i]
        start = nhltime.subtract_30_minutes(start)
        end = nhltime.add210minutes(start)
        df['Start Time'][i] = nhltime.est_to_utc(start)
        df.at[i, 'End Time'] = nhltime.est_to_utc(end)
    return df

# Cleans the network column and adds a channel id column
def clean_networks(df:pandas.DataFrame) -> pandas.DataFrame:
    df['Network'] = df['Network'].str.split(',')
    df = df.explode('Network')
    df = df.reset_index(drop = True)
    id = {}
    path = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/nhl/nhl-data/nhl-text-files/nhl-broadcast.txt'
    file = open(path, 'r')
    for line in file:
        key, value = line.rstrip().split(': ')
        id[key] = value
    for i in range(len(df)):
        df['Network'][i] = str(df['Network'][i]).join(str(df['Network'][i]).split())
        if df['Network'][i] in id:
            df.at[i, 'Channel ID'] = id[df['Network'][i]]
    return df

# Adds a sport column to the data frame
def add_sport(df) -> pandas.DataFrame:
    df['Sport'] = ['HockeyPlayoff'] * len(df)
    return df

# Reorders the data frame columns
def reorder_columns(df:pandas.DataFrame) -> pandas.DataFrame:
    # Reorder the data frame columns
    df = df.reindex(columns = ['Subject', 'Date', 'Network', 'Channel ID', 'Start Time', 'End Time', 'Sport', 'Home Team', 'Away Team'])
    return df

# Cleans the data frame
def clean(df:pandas.DataFrame) -> pandas.DataFrame:
    # Clean the data frame
    df = clean_subject(df)
    df = clean_times(df)
    df = clean_networks(df)
    df = add_sport(df)
    df = reorder_columns(df)
    return df