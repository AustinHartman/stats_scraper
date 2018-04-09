# stats_scraper
Stat scraper which scrapes data from basketball-reference.com 
hopefully will soon be expanded to other sports branching from 
sports-reference.com 

Files Included:
learn2.py:            functions used to scrape from basketball-reference.com
			          Note: last tested 04/07/2018 but if website HTML tags were
			          to change files would need updates.
			          Note: file needs to be renamed to be more informative
			          
team_ratings.py       includes functions to compile csv of ever shot a player 
                      took in a season as well as advanced shooting stats by
                      season
                      Note: need to rename file b/c doesnt pertain to team
                      ratings

steph_2015_2016_shooting.csv csv of steph curry's 2015-2016 advanced shooting
							 stats.
						
steph_2015_2016_every_shot.csv csv containing data on each shot taken by steph
							   in the 2015-2016 nba season.
			  
nba.csv:              created using functions in learn2.py to create csv of basic
		              career stats (ppg, rbpg, efg%, etc. ) of every active NBA
		              player as of 04/07/2018
		      
warriros.csv:         also created using learn2.py and gives same career statistics
                      but only for active players on the warriors as of 04/07/2018
              
klay_thompson.csv
stephen_curry.csv
shaun_livingston.csv: each csv contains the career statistics for the
					  given player
					  
