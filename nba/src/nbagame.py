from bs4 import BeautifulSoup
class NbaGame:
    
    # Default constructor
    def __init__(self, date:str, html:str):
        self.date = date
        self.html = html
        self.subject = self.scrape_subject()
        self.networks = self.scrape_networks()
        self.time = self.scrape_time()
        self.location = self.scrape_location()

    # Scrapes the game subjects
    def scrape_subject(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        subject_html = soup.find_all('div', class_ = 'ScheduleGame_sgTeam__TEPZa')
        subjects = [info.find('a', class_ = 'Anchor_anchor__cSc3P Link_styled__okbXW').get_text() for info in subject_html]
        return subjects[0] + ' vs. ' + subjects[1]
    
    # Scrapes the game broadcast networks
    def scrape_networks(self) -> list:
        networks = []
        soup = BeautifulSoup(self.html, "html.parser")
        networkhtml = soup.find_all('div', class_= 'Broadcasters_section__ISlyP')[:-1]
        if len(networkhtml) > 0:
            if networkhtml[0].find('img', title = 'TNT'):
                networks.append('TNT')
            elif networkhtml[0].find('img', title = 'ABC'):
                networks.append('ABC')
            elif networkhtml[0].find('img', title = 'ESPN'):
                networks.append('ESPN')
            elif networkhtml[0].find('img', title = 'NBA TV'):
                networks.append('NBA TV')
            elif networkhtml[0].find('img', title = 'LEAGUE PASS'):
                networks.append('NBA League Pass')
        if len(networkhtml) == 2:
            networks.extend([element.text for element in networkhtml[1].find_all('span', class_ = 'Broadcasters_tv__AIeZb')])
            networks.extend([element.text for element in networkhtml[1].find_all('a', class_ = 'Anchor_anchor__cSc3P Broadcasters_tv__AIeZb')])
        return networks
    
    # Scrapes the game time
    def scrape_time(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        return soup.find('span', class_ = 'ScheduleStatusText_base__Jgvjb').text

    # Scrapes the game location
    def scrape_location(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        location = soup.find('div', class_ = "ScheduleGame_sgLocationInner__xxr0Z").get_text('\n')
        arena, city = location.split('\n')
        return arena + ' - ' + city