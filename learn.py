#BASED ON TUTORIAL FROM LINK BELOW
#https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
#

# import libraries
import urllib3
from bs4 import BeautifulSoup

# specify the url
quote_page = "http://www.bloomberg.com/quote/SPX:IND"

# query the website and return the html to the variable ‘page’
page = urllib3.urlopen(quote_page)
urllib3.