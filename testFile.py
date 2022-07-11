from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
import numpy as np
import pandas as pd
from datetime import date

leagues = ["https://www.flashscore.dk/fodbold/england/premier-league/resultater/"]

# 'https://www.flashscore.dk/fodbold/england/championship/resultater/',
# 'https://www.flashscore.dk/fodbold/danmark/superliga/resultater/',
# 'https://www.flashscore.dk/fodbold/frankrig/ligue-1/resultater/',
# 'https://www.flashscore.dk/fodbold/italien/serie-a/resultater/',
# 'https://www.flashscore.dk/fodbold/spanien/laliga/resultater/',
# 'https://www.flashscore.dk/fodbold/tyskland/bundesliga/resultater/'

for i,league in enumerate(leagues):
# URL =
    leagueName = league.split('/')[-3]#.replace('-','_')
    # Use sync version of Playwright
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch()

        # Open a new browser page
        page = browser.new_page()

        # Create a URI for our test file
        # page_path = "file://" + os.getcwd() + "/test.html"

        # Open our test file in the opened page
        page.goto(league)
        page.wait_for_timeout(5000)

        ## Initiate
        MoreToClick = True
        while MoreToClick:
            try:
                page.click('text=Vis flere kampe')
            except:
                MoreToClick = False
            
        page_content = page.content()

        # Process extracted content with BeautifulSoup
        soup = BeautifulSoup(page_content)
        content = soup.find(id='live-table')
        # print(content.prettify())

        ## Attempt on extracting all the games
        games = soup.find_all('div', class_=["event__match event__match--static event__match--twoLine",
                                                "event__match event__match--static event__match--last event__match--twoLine"])
        # print(soup.find(id="test").get_text())
        # print(len(games))

        timestampList=[] #List to store name of the product
        hometeamList=[] #List to store price of the product
        awayteamList=[] #List to store rating of the product
        homegoalList=[] #List to store price of the product
        awaygoalList=[] #List to store rating of the product

        for game in games:
            # print(game, end='\n'*2)

            timestamp=game.find('div',class_="event__time").text
            hometeam=game.find('div',class_="event__participant--home").text# event__participant--home fontBold
            awayteam=game.find('div',class_="event__participant--away").text
            homegoal=game.find('div',class_="event__score--home").text#event__score--home
            awaygoal=game.find('div',class_="event__score--away").text

            ## Appending to the lists
            timestampList.append(timestamp)
            hometeamList.append(hometeam)
            awayteamList.append(awayteam)
            homegoalList.append(homegoal)
            awaygoalList.append(awaygoal)

        df = pd.DataFrame({'Timestamp':timestampList,
                        'Home team':hometeamList,
                        'Away team':awayteamList,
                        'Goal (home)':homegoalList,
                        'Goal (away)':awaygoalList})

        if os.path.isdir('data/'+str(date.today())):
            if i == 0:
                print('Date folder already in place.\n\nSaving the data..\n\n')

        else:
            print('Creating folder..\n')
            ## Create the folder to save the data
            os.mkdir('data/'+str(date.today()))
            # print(leagueName)
        print('Saving data on '+leagueName + '..\n')
            # Save the data
        df.to_excel('data/'+str(date.today())+'/'+leagueName+'.xlsx')

        #### Below happens in the notebook going forward

        # teams = df.loc[:,'Home team'].unique()
        #
        # avgGoalsHomeList = []
        # avgGoalsAwayList = []
        # avgLastFiveList = []
        # lastFiveList = []
        # lastFiveHomeList = []
        # lastFiveAwayList = []
        #
        # # testSeries = pd.Series()#index=np.arange(len(teams))
        # # print(testSeries)
        # for i,team in enumerate(teams):
        #
        #     teamStats = df[(df.loc[:,'Home team']==team) | (df.loc[:,'Away team']==team)]
        #     homeGames = df[df.loc[:,'Home team']==team]
        #     awayGames = df[df.loc[:,'Away team']==team]
        #
        #     lastFive = teamStats.head(5)
        #     lastFiveHome = homeGames.head(5)
        #     lastFiveAway = awayGames.head(5)
        # # print(df[df.loc[:,'Home team']=='Arsenal'])
        #     goalsHome = homeGames.loc[:,'Goal (home)'].astype(int)
        #     goalsAway = awayGames.loc[:,'Goal (away)'].astype(int)
        #
        #     avgGoalsHome = goalsHome.sum()/min(goalsHome.shape[0],5)
        #     avgGoalsAway = goalsAway.sum()/min(goalsAway.shape[0],5)
        #
        #     allGoals = pd.concat([goalsHome,goalsAway])
        #     sortedIndex = allGoals.index.sort_values()
        #
        #     avgLastFive = allGoals[sortedIndex][0:5].sum()/min(allGoals.shape[0],5)
        #
        #     avgGoalsHomeList.append(avgGoalsHome)
        #     avgGoalsAwayList.append(avgGoalsAway)
        #     avgLastFiveList.append(avgLastFive)
        #     lastFiveList.append(lastFive)
        #     lastFiveHomeList.append(lastFiveHome)
        #     lastFiveAwayList.append(lastFiveAway)
        #     # testSeries.iloc[str(i)] = lastFive
        #     # testSeries.append(lastFive)
        # # print(lastFive)
        # # print(lastFiveHome)
        # # print(lastFiveAway)
        # # print(testSeries)
        # # print(lastFiveList[0:2],end='\n'*2)
        # # print(lastFiveHome[0:2])
        # # print(lastFiveAwayList[0:2])
        # # print(df[(df.loc[:,'Home team']==team) | (df.loc[:,'Away team']==team)])
        # # # print(goalsHome)
        # # print(avgLastFive)
        # # print(allGoals[sortedIndex][0:5])
        # # print(min(allGoals.shape[0],5))
        #
        # # print(allGoals.index)
        # # print(allGoals.index.sort_values())
        # # print(allGoals[sortedIndex])
        # overview = pd.DataFrame({'Team':teams,
        #                             'AvgGoalsHome':avgGoalsHomeList,
        #                             'avgGoalsAway':avgGoalsAwayList,
        #                             'avgLastFive':avgLastFiveList
        #                             }
        #                         ).sort_values('Team').reset_index(drop=True).round(2)
        #
        # overviewGames = pd.DataFrame({'Team':teams,
        #                                 'LastFive':lastFiveList,
        #                                 'LastFiveHome':lastFiveHomeList,
        #                                 'LastFiveAway':lastFiveAwayList
        #                             }
        #                         ).sort_values('Team').reset_index(drop=True)
        #
        # print(overview,end='\n'*2)

        # print(overviewGames,end='\n'*2)
        # print(overviewGames[overviewGames.loc[:,'Team']=='Arsenal'],end='\n'*2)#.LastFive
        # print(overviewGames[overviewGames.Team=='Arsenal'].LastFiveHome,end='\n'*2)
        # print(overviewGames[overviewGames.Team=='Arsenal'].LastFiveAway,end='\n'*2)

        # print(df[df.loc[:,'Home team']=='Arsenal'].loc[:,['Goal (home)','Goal (away)']].shape)
        # print(pd.DataFrame({'Timestamp':timestampList,
        #                 'Home team':hometeamList,
        #                 'Away team':awayteamList,
        #                 'Goal (home)':homegoalList,
        #                 'Goal (away)':awaygoalList}))
        # Close browser
        browser.close()
