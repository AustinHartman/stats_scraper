import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import requests
import csv


def clear(file):
    table = open(file, 'w')
    table.close()


def add_headers(file):
    stats = ['id', 'player_name', 'season', 'age', 'team', 'pos', 'games', 'games_started', 'mpg', 'fg_per_g', 'fga_per_g',
             'fg_pct', 'fg3_per_g', 'fg3_pct', 'fg2_per_g', 'fg2a_per_g', 'fg2_pct', 'efg_pct',
             'ft_per_g', 'fta_per_g', 'ft_pct', 'orb_per_g', 'drb_per_g', 'trb_per_g', 'ast_per_g',
             'stl_per_g', 'blk_per_g', 'tov_per_g', 'pf_per_g', 'pts_per_g']
    table = open(file, 'w')
    a = csv.writer(table)
    a.writerow(stats)
    table.close()


row_id = -1


def player_csv(url, file, edit='w'):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    name = soup.find("h1", attrs={"itemprop": "name"}).text
    years = soup.find_all('tr', 'full_table')

    # changing the 'w' to 'a' allows me to append to the file instead of rewrite
    table = open(file, edit)
    a = csv.writer(table)

    global row_id

    for year in years:
        data = []

        row_id += 1
        data.append(row_id)
        data.append(name)

        data.append(year.find(attrs={"data-stat": "season"}).text)
        data.append(year.find(attrs={"data-stat": "age"}).text)
        data.append(year.find(attrs={"data-stat": "team_id"}).text)
        data.append(year.find(attrs={"data-stat": "pos"}).text)
        data.append(year.find(attrs={"data-stat": "g"}).text)
        data.append(year.find(attrs={"data-stat": "gs"}).text)
        data.append(year.find(attrs={"data-stat": "mp_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "fg_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "fga_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "fg_pct"}).text)
        data.append(year.find(attrs={"data-stat": "fg3_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "fg3_pct"}).text)
        data.append(year.find(attrs={"data-stat": "fg2_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "fg2a_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "fg2_pct"}).text)
        data.append(year.find(attrs={"data-stat": "efg_pct"}).text)
        data.append(year.find(attrs={"data-stat": "ft_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "fta_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "ft_pct"}).text)
        data.append(year.find(attrs={"data-stat": "orb_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "drb_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "trb_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "ast_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "stl_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "blk_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "tov_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "pf_per_g"}).text)
        data.append(year.find(attrs={"data-stat": "pts_per_g"}).text)

        a.writerow(data)

        print(data)

    table.close()


def get_players(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    players = soup.find_all("tr")
    return players


def get_team_stats(players, file):
    for player in players[1:]:
        player_csv('https://www.basketball-reference.com'+(player.find('a', href=True))['href'], file, 'a')


def get_teams_east(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    east_teams = soup.find('div', attrs={"id": "all_confs_standings_E"}).find_all('tr')
    return east_teams


def get_teams_west(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    west_teams = soup.find('div', attrs={"id": "all_confs_standings_W"}).find_all('tr')
    return west_teams


def compile_csv(teams):
    for team in teams[1:]:
        print(team)
        players = get_players('https://www.basketball-reference.com' + (team.find('a', href=True))['href'])
        get_team_stats(players, 'nba.csv')


clear("nba.csv")
add_headers("nba.csv")
compile_csv(get_teams_east("https://www.basketball-reference.com/leagues/NBA_2018.html"))
compile_csv(get_teams_west("https://www.basketball-reference.com/leagues/NBA_2018.html"))