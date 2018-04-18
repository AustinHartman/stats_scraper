from bs4 import BeautifulSoup, Comment
import requests
import csv

"""
Main methods to use in player class are get_current_attributes
and every_shot_in_season. 
get_current_attributes adds line in a csv containing basic statistical info
every_shot_in_season collects data on every single shot a player took in a
given season
"""


# Player class grabs basic statistical attributes on a player typically to be then loaded into a csv of many players
class Player:
    def __init__(self, url):
        self.url = url;

    # Returns 1-2 char pos key (used in getAttributes method)
    def get_position(s):
        if s == "Point":
            return "PG"
        elif s == "Small":
            return "SF"
        elif s == "Shooting":
            return "SG"
        elif s == "Center":
            return "C"
        else:
            return "PF"

    def getCurrentAttributes(self, file):
        # atrributes = [name, height(cm), weight(kg), position,
        #               games, pts, trb, ast, fg_pct,
        #               fg3_pct, ft_pct, efg, per, ws]
        attributes = []
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")

        table = open(file, 'a')
        a = csv.writer(table)

        try:
            name = soup.find("h1", attrs={"itemprop": "name"}).text
            attributes.append(name)
            paras = soup.find_all("p")
            position = ""
            for p in paras:
                separate = ""
                if "Position:" in p.text:
                    position = Player.get_position(p.text.split()[1])
                elif "lb" in p.text and "kg)" in p.text:
                    separate = p.text.split()
                    attributes.append(float(separate[2][1:4]))
                    attributes.append(float(separate[3][:-3]))
                    break
            attributes.append(position)
            stats = soup.find("div", "stats_pullout").find_all("div")

            for stat in stats[3:7]:
                if stat.find("p").text == '-':
                    val = None
                else:
                    val = float(stat.find("p").text)
                attributes.append(val)

            for stat in stats[8:13]:
                if stat.find("p").text == '-':
                    val = None
                else:
                    val = float(stat.find("p").text)
                attributes.append(val)

            if stats[14].find("p").text == '-':
                val = None
            else:
                val = float(stats[14].find("p").text)
            attributes.append(val)            
        except:
            l = len(attributes)
            for i in range(14-l):
                attributes.append(None)

        a.writerow(attributes)
        table.close()

    # All below get functions are for use in season_shot_by_shot
    def get_date(s):
        d = s[0].split(",")
        return d[0] + "," + d[1]

    def get_game(s):
        return s[0].split(",")[-1]

    def get_made(s):
        return s[2].split(" ")[0]

    def get_dist(s):
        return s[2].split(" ")[3]

    def get_value(s):
        return s[2].split(" ")[1][0]

    def get_score(s):
        return s[3].split(" ")[-1]

    def get_shooting_url(self, year):
        return self.url[:-5] + "/shooting/" + str(year)

    # Write every single shot a player took in a season to a CSV
    def every_shot_in_season(self, file, year):
        page = requests.get(Player.get_shooting_url(self, year))

        # changing the 'w' to 'a' allows me to append to the file instead of rewrite
        table = open(file, 'a')
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
                    data.append(Player.get_date(s))
                    data.append(Player.get_game(s))
                    data.append(Player.get_value(s))
                    data.append(Player.get_dist(s))
                    data.append(Player.get_made(s))
                    data.append(Player.get_score(s))

                    a.writerow(data)
        table.close()

    def every_shot_in_career(self, file):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")
        stats_table = soup.find("div", attrs={"id": "all_per_game"}).find_all("tr", "full_table")
        for year in stats_table:
            # current year split in format ex. 2000-01, and link for this season uses 2001 in the url
            current_year_split = year.find("th").text
            current_year = current_year_split[:2] + current_year_split[-2:]
            Player.every_shot_in_season(self, file, current_year)

    # collect data from each season of a players career and write it to a CSV
    def player_csv(self, file, edit='a'):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")
        name = soup.find("h1", attrs={"itemprop": "name"}).text
        years = soup.find_all('tr', 'full_table')

        # changing the 'w' to 'a' allows me to append to the file instead of rewrite
        table = open(file, edit)
        a = csv.writer(table)

        for year in years:
            data = []
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
        table.close()


def clear(file):
    table = open(file, 'w')
    table.close()

clear("example_csvs/steph_every_shot.csv")

steph = Player("https://www.basketball-reference.com/players/c/curryst01.html")
steph.every_shot_in_career("example_csvs/steph_every_shot.csv")