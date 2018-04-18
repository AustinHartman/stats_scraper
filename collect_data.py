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
    # commented out stats arrays represent other headers commonly used with Player class functions
    stats = ['name', 'height(cm)', 'weight(kg)', 'position', 'games', 'pts', 'trb', 'ast', 'fg_pct',  'fg3_pct', 'ft_pct', 'efg', 'per', 'ws']
    '''
    stats = ['player_name', 'season', 'age', 'team', 'pos', 'games', 'games_started', 'mpg', 'fg_per_g', 'fga_per_g',
             'fg_pct', 'fg3_per_g', 'fg3_pct', 'fg2_per_g', 'fg2a_per_g', 'fg2_pct', 'efg_pct',
             'ft_per_g', 'fta_per_g', 'ft_pct', 'orb_per_g', 'drb_per_g', 'trb_per_g', 'ast_per_g',
             'stl_per_g', 'blk_per_g', 'tov_per_g', 'pf_per_g', 'pts_per_g']
    stats = ['date', 'game', 'value', 'distance', 'made', 'score']
    '''

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


compile_csv(get_teams_east("https://www.basketball-reference.com/leagues/NBA_2018.html"))
compile_csv(get_teams_west("https://www.basketball-reference.com/leagues/NBA_2018.html"))

