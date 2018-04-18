from player import Player
from bs4 import BeautifulSoup, SoupStrainer
import requests
import csv

# USE WITH CAUTION... Cycling through NBA with player class takes ~10 minutes so clearing
# on accident is costly
def clear(file):
    table = open(file, 'w')
    table.close()

#clear('example_csvs/nba_plyr_reg_season_stats.csv')

# array stats represents headers in csv which is about to be compiled
def add_headers(file):
    stats = ['name', 'height(cm)', 'weight(kg)', 'position', 'games', 'pts', 'trb', 'ast', 'fg_pct',  'fg3_pct', 'ft_pct', 'efg', 'per', 'ws']
    table = open(file, 'w')
    a = csv.writer(table)
    a.writerow(stats)
    table.close()

#add_headers('example_csvs/nba_plyr_reg_season_stats.csv')

# get all players from bball_ref team roster url
def get_players(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    players = soup.find_all("tr")
    return players


# loop through roster player by player and call Player class to scrape stats
def get_team_stats(players, file):
    table = open(file, 'a')
    a = csv.writer(table)
    for player in players[1:]:
        data = Player('https://www.basketball-reference.com'+(player.find('a', href=True))['href']).getAttributes()
        a.writerow(data)
    table.close()


# get all of the teams in the east
def get_teams_east(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    east_teams = soup.find('div', attrs={"id": "all_confs_standings_E"}).find_all('tr')
    return east_teams


# get all of the teams in the west
def get_teams_west(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    west_teams = soup.find('div', attrs={"id": "all_confs_standings_W"}).find_all('tr')
    return west_teams


# take a list of teams and cycle through individual rosters, at each team call get_players which calls Player class to scrape player stats
def compile_csv(teams, file):
    for team in teams[1:]:
        print(team)
        players = get_players('https://www.basketball-reference.com' + (team.find('a', href=True))['href'])
        get_team_stats(players, file)

