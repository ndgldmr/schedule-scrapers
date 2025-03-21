import nbatime
import pandas

# Cleans the network column
def networks(df:pandas) -> pandas:
    for i in range(len(df)):
        df['Networks'][i] = df['Networks'][i].translate({ord(c): None for c in "'[]"})
    df['Networks'] = df['Networks'].str.split(', ')
    df = df.explode('Networks')
    df = df.reset_index(drop=True)
    return df

# Cleans the start/end date-time columns
def times(df:pandas) -> pandas:
    df = df.rename(columns={'Time': 'Start Time (UTC)'})
    df['Start Time (UTC)'] = df['Start Time (UTC)'].apply(nbatime.time24hour)
    for i in range(len(df)):
        df['Start Time (UTC)'][i] = df['Date'][i] + ' ' + df['Start Time (UTC)'][i]
    df['Start Time (UTC)'] = df['Start Time (UTC)'].apply(nbatime.subtract30minutes)
    df['End Time (UTC)'] = df['Start Time (UTC)'].apply(nbatime.add210minutes)
    df['Start Time (UTC)'] = df['Start Time (UTC)'].apply(nbatime.utc)
    df['End Time (UTC)'] = df['End Time (UTC)'].apply(nbatime.utc)
    return df

# Adds a channel id column to each row
def channelids(df:pandas) -> pandas:
    for i in range(len(df)):
        file = open('/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/nba/nba-data/nba-text-files/nba-channels.txt', 'r')
        for line in file:
            key, value = line.rstrip().split(' - ')
            if df['Networks'][i] ==  key:
                df.at[i, 'Channel ID'] = value
                break
    return df

# Adds a home/away team column
def teams(df:pandas) -> pandas:
    for i in range(len(df)):
        subject = df.at[i, 'Subject']
        away_team, home_team = subject.split(' vs. ', 2)
        df.at[i, 'Away Team'] = away_team
        df.at[i, 'Home Team'] = home_team
    return df

# Add the sport
def sport(df:pandas) -> pandas:
    for i in range(len(df)):
        df.at[i, 'Sport'] = 'BasketballPlayoff'
    return df

# Reorders the data frame columns
def reorder(df:pandas) -> pandas:
    order = ['Subject', 'Date', 'Location', 'Networks', 'Channel ID', 'Start Time (UTC)', 'End Time (UTC)', 'Sport', 'Home Team', 'Away Team']
    df = df.reindex(columns= order)
    return df

# Cleans the data frame
def clean(df:pandas.DataFrame) -> pandas.DataFrame:
    df = networks(df)
    df = channelids(df)
    df = times(df)
    df = teams(df)
    df = sport(df)
    df = reorder(df)
    df = df.replace({'Home Team': 'LA Clippers'}, {'Home Team': 'Los Angeles Clippers'})
    df = df.replace({'Away Team': 'LA Clippers'}, {'Away Team': 'Los Angeles Clippers'})
    return df

# Driver
def main():
    filepath = input('Enter the path to your schedule file: ')
    df = pandas.read_csv(filepath, index_col = 0)
    df = clean(df)
     # Save the cleaned schedule to a CSV file
    folderpath = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/nba/nba-data/processed-nba-data'
    filename = filepath.split('/')[9].replace('raw', 'processed')
    df.to_csv(folderpath + '/' + filename)

# Driver call
if __name__ == '__main__':
    main()