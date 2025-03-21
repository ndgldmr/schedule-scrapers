import pandas 
import mlbtime

# Cleans the team columns
def clean_teams(df:pandas.DataFrame) -> pandas.DataFrame:
    file = open('/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/mlb/mlb-data/mlb-info/mlb-teams.txt', 'r')
    team_names = {line.split(',')[0] : line.strip().split(',')[1] for line in file}
    subjects, away_teams, home_teams = [], [], []
    for i in range(len(df)):
        away_team, home_team = df['Subject'][i].split(' @ ')  
        subjects.append(team_names[away_team] + ' vs. ' + team_names[home_team])
        away_teams.append(team_names[away_team])
        home_teams.append(team_names[home_team])
    df['Subject'] = subjects
    df['Away Team'] = away_teams
    df['Home Team'] = home_teams
    return df

# Cleans the time columns
def clean_times(df:pandas.DataFrame) -> pandas.DataFrame:
    df = df.rename(columns = {'Time': 'Start Time (UTC)'})
    df['Start Time (UTC)'] = df['Start Time (UTC)'].apply(mlbtime.time_24hour)
    for i in range(len(df)):
        df['Start Time (UTC)'][i] = df['Date'][i] + ' ' + df['Start Time (UTC)'][i]
    df['Start Time (UTC)'] = df['Start Time (UTC)'].apply(mlbtime.subtract_30minutes)
    df['End Time (UTC)'] = df['Start Time (UTC)'].apply(mlbtime.add_4hours)
    df['Start Time (UTC)'] = df['Start Time (UTC)'].apply(mlbtime.est_to_utc)
    df['End Time (UTC)'] = df['End Time (UTC)'].apply(mlbtime.est_to_utc)
    return df

# Cleans the network columns
def clean_networks(df:pandas.DataFrame) -> pandas.DataFrame:
    df['Networks'] = df['Networks'].str.split(', ')
    df = df.explode('Networks')
    df = df.reset_index(drop = True)
    file = open('/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/mlb/mlb-data/mlb-info/mlb-networks.txt', 'r')
    networks = {line.split(',')[0] : line.strip().split(',')[1] for line in file}
    channel_ids = []
    for i in range(len(df)):
        channel_ids.append(networks[df['Networks'][i]])
    df['Channel ID'] = channel_ids
    return df

# Add a sport column
def clean_sport(df:pandas.DataFrame) -> pandas.DataFrame:
    sport = ['Baseball'] * len(df)
    df['Sport'] = sport
    return df

# Reorders the columns
def reorder(df:pandas.DataFrame) -> pandas.DataFrame:
    order = ['Subject', 'Date', 'Networks', 'Channel ID', 'Start Time (UTC)', 'End Time (UTC)', 'Sport', 'Home Team', 'Away Team']
    df = df.reindex(columns= order)
    return df

# Cleans the schedule
def clean(df:pandas.DataFrame) -> pandas.DataFrame:
    df = clean_teams(df)
    df = clean_times(df)
    df = clean_networks(df)
    df = clean_sport(df)
    df = reorder(df)
    return df

# Driver
def main():
    # Clean the schedule at the specified file path
    filepath = input('Enter the file path: ')
    df = pandas.read_csv(filepath)
    df = clean(df)
    # Save the cleaned schedule to a CSV file
    folderpath = '/Users/nathanielgoldammer/Documents/zoomph-src/schedule-pipeline/mlb/mlb-data/mlb-processed'
    filename = filepath.split('/')[9].replace('raw', 'processed')
    df.to_csv(folderpath + '/' + filename)

# Driver call
if __name__ == '__main__':
    main()