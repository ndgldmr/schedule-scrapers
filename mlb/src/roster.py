import requests
from bs4 import BeautifulSoup
import pandas

response = requests.get('https://www.espn.com/mlb/team/roster/_/name/sf/san-francisco-giants')
html = response.content
soup = BeautifulSoup(html, 'html.parser')

tables = soup.find_all('table')
dfs = [pandas.read_html(str(table))[0] for table in tables]
df = pandas.concat(dfs)
df.drop(columns=['Unnamed: 0', 'POS', 'BAT', 'THW', 'Age', 'HT', 'WT', 'Birth Place'], inplace=True)
df.reset_index(inplace=True)
for i in range(len(df)):
    df['Name'][i] = df['Name'][i][:-2]
df.drop(columns=['index'], inplace=True)
df.to_csv('san-francisco-giants.csv')