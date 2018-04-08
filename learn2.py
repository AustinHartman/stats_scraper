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


def player_csv(url, file, edit):
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


        season = year.find(attrs={"data-stat": "season"}).text
        age = year.find(attrs={"data-stat": "age"}).text
        team = year.find(attrs={"data-stat": "team_id"}).text
        pos = year.find(attrs={"data-stat": "pos"}).text
        games = year.find(attrs={"data-stat": "g"}).text
        games_started = year.find(attrs={"data-stat": "gs"}).text
        mpg = year.find(attrs={"data-stat": "mp_per_g"}).text
        fg_per_g = year.find(attrs={"data-stat": "fg_per_g"}).text
        fga_per_g = year.find(attrs={"data-stat": "fga_per_g"}).text
        fg_pct = year.find(attrs={"data-stat": "fg_pct"}).text
        fg3_per_g = year.find(attrs={"data-stat": "fg3_per_g"}).text
        fg3_pct = year.find(attrs={"data-stat": "fg3_pct"}).text
        fg2_per_g = year.find(attrs={"data-stat": "fg2_per_g"}).text
        fg2a_per_g = year.find(attrs={"data-stat": "fg2a_per_g"}).text
        fg2_pct = year.find(attrs={"data-stat": "fg2_pct"}).text
        efg_pct = year.find(attrs={"data-stat": "efg_pct"}).text
        ft_per_g = year.find(attrs={"data-stat": "ft_per_g"}).text
        fta_per_g = year.find(attrs={"data-stat": "fta_per_g"}).text
        ft_pct = year.find(attrs={"data-stat": "ft_pct"}).text
        orb_per_g = year.find(attrs={"data-stat": "orb_per_g"}).text
        drb_per_g = year.find(attrs={"data-stat": "drb_per_g"}).text
        trb_per_g = year.find(attrs={"data-stat": "trb_per_g"}).text
        ast_per_g = year.find(attrs={"data-stat": "ast_per_g"}).text
        stl_per_g = year.find(attrs={"data-stat": "stl_per_g"}).text
        blk_per_g = year.find(attrs={"data-stat": "blk_per_g"}).text
        tov_per_g = year.find(attrs={"data-stat": "tov_per_g"}).text
        pf_per_g = year.find(attrs={"data-stat": "pf_per_g"}).text
        pts_per_g = year.find(attrs={"data-stat": "pts_per_g"}).text

        data.append(season)
        data.append(age)
        data.append(team)
        data.append(pos)
        data.append(games)
        data.append(games_started)
        data.append(mpg)
        data.append(fg_per_g)
        data.append(fga_per_g)
        data.append(fg_pct)
        data.append(fg3_per_g)
        data.append(fg3_pct)
        data.append(fg2_per_g)
        data.append(fg2a_per_g)
        data.append(fg2_pct)
        data.append(efg_pct)
        data.append(ft_per_g)
        data.append(fta_per_g)
        data.append(ft_pct)
        data.append(orb_per_g)
        data.append(drb_per_g)
        data.append(trb_per_g)
        data.append(ast_per_g)
        data.append(stl_per_g)
        data.append(blk_per_g)
        data.append(tov_per_g)
        data.append(pf_per_g)
        data.append(pts_per_g)

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