from bs4 import BeautifulSoup, Comment
import requests
import csv

# Player class grabs basic statistical attributes on a player typically to be then loaded into a csv of many players
class Player:
    def __init__(self, url):
        self.url = url;

    # Returns 1-2 char pos key (used in getAttributes method)
    def getPosition(s):
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

    def getAttributes(self):
        # atrributes = [name, height(cm), weight(kg), position,
        #               games, pts, trb, ast, fg_pct,
        #               fg3_pct, ft_pct, efg, per, ws]
        attributes = []
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")

        #find name
        name = soup.find("h1", attrs={"itemprop": "name"}).text
        attributes.append(name)

        try:
            paras = soup.find_all("p")
            position = ""
            for p in paras:
                separate = ""
                if "Position:" in p.text:
                    position = Player.getPosition(p.text.split()[1])
                elif "lb" in p.text:
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
                print(attributes)

            for stat in stats[8:13]:
                if stat.find("p").text == '-':
                    val = None
                else:
                    val = float(stat.find("p").text)
                attributes.append(val)
                print(attributes)

            if stats[14].find("p").text == '-':
                val = None
            else:
                val = float(stats[14].find("p").text)
            attributes.append(val)
        except:
            None

        return attributes





