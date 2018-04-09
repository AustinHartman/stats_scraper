from bs4 import BeautifulSoup, Comment
import requests
import csv


def clear(file):
    table = open(file, 'w')
    table.close()


def add_headers_shooting_stats(file):
    stats = ['split', 'value', 'fg', 'fga', 'fg_pct',
             '3pm', '3pma', '3p_pct', 'efg_pct',
             'astd', 'astd_pct']
    table = open(file, 'w')
    a = csv.writer(table)
    a.writerow(stats)


def add_headers_shots_taken(file):
    stats = ['date', 'game', 'value', 'distance', 'made', 'score']
    table = open(file, 'w')
    a = csv.writer(table)
    a.writerow(stats)


def player_csv_shooting(url, file, edit='w'):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    rows = soup.find_all("tr")

    # changing the 'w' to 'a' allows me to append to the file instead of rewrite
    table = open(file, edit)
    a = csv.writer(table)

    for row in rows:
        data = []

        th = row.find('th').text
        data.append(th)

        h = row.find_all("td")
        for i in h:
            data.append(i.text)

        a.writerow(data)

    table.close()


def getDate(s):
    d = s[0].split(",")
    return d[0] + "," + d[1]


def getGame(s):
    return s[0].split(",")[-1]


def getMade(s):
    return s[2].split(" ")[0]


def getDist(s):
    return s[2].split(" ")[3]


def getValue(s):
    return s[2].split(" ")[1][0]


def getScore(s):
    return s[3].split(" ")[-1]


def season_shot_by_shot(url, file, edit):
    page = requests.get(url)

    # changing the 'w' to 'a' allows me to append to the file instead of rewrite
    table = open(file, edit)
    a = csv.writer(table)

    soup = BeautifulSoup(page.content, "lxml")
    comment_lines = soup.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comment_lines:
        soup = BeautifulSoup(comment, "lxml")
        divs = soup.find_all('div', tip=True)
        if len(divs) > 0:
            for div in divs:
                data = []
                s = str(div['tip']).split("<br>")
                data.append(getDate(s))
                data.append(getGame(s))
                data.append(getValue(s))
                data.append(getDist(s))
                data.append(getMade(s))
                data.append(getScore(s))

                a.writerow(data)
    table.close()