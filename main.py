# Import scraping modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3 as sq	
from random import randint


# Setting selenium to headless mode, so that the browser wont open up during scraping process
cm = Options()
cm.add_argument("--headless")
DRIVER_PATH = 'C:\Miscellaneous\chromedriver_win32\chromedriver.exe'
WEEK = 4


# QB Index Lookup: Passing Yards = 8; touchdowns = 20; Rush Atempts = 16, Rush Yards = 17, 
QB_Lookup = {'PassYds': 8, 'Tds': 20, 'RushAtempts': 16, 'RushYds': 17}
# RB Index Lookup: Receptions = 11; Rec Yds = 12; Rush Atempts = 6; Rush Yards = 7; Touchdowns = 17
RB_Lookup = {'RushAtempts': 6, 'RushYds': 7, 'Rec': 11, 'RecYds': 12, 'Tds': 17}
# WB Index Lookup: Receptions = 7; Rec Yds = 8; Touchdowns = 14
WR_Lookup = {'Rec': 7, 'RecYds': 8, 'Tds': 14}

# allData = {'JDOG': [], 'MOMMASBOYS': [], 'DOCSDYNASTY': [], 'GROUNDCHUCK': [], 'HALLELUJAHHARKERS': [], 'LOGANASUARUS': [], 'JOSJOCKS': [], 'RADSRADICALS': []}
allData = {'JDOG': [], 'MOMMASBOYS': []}

def create_playerids(nflTeamIds):
    allPlayerIds = []

    # URL of page
    for team in nflTeamIds:
        url = f'https://www.pro-football-reference.com/teams/{team}/2021_roster.htm'
        browser = webdriver.Chrome(DRIVER_PATH, options=cm)
        browser.get(url)

        element = browser.find_element_by_class_name("table_container").find_elements_by_xpath("//td[1]")
        
        for i in range(len(element)-1):
            allPlayerIds.append(element[i].find_element_by_tag_name('a').get_attribute('href').split('/')[5][:8])
            
        browser.quit()
        
    return allPlayerIds
        
        
def create_player_info(pIds):  
    # print(pIds) 
    # temp_pIds = pIds[0]   
    for id in pIds:
        print(id)
        url = f'https://www.pro-football-reference.com/players/{id[0]}/{id}/gamelog/2021/'
        browser = webdriver.Chrome(DRIVER_PATH, options=cm)
        browser.get(url)
                
        element = browser.find_element_by_id("div_stats").find_elements_by_xpath(f"//tr[{WEEK}]")
        
        for i in element[1].find_elements_by_class_name("right"):
            print(i.text)

def fill_teams(data):
    t = input("If creating new leauge press n: ")
    if (t == 'n'):
        for team in data:
            print(f'Current Team: {team}')
            data[team].append(input('Enter QB1: '))
            data[team].append(input('Enter QB2: '))
            data[team].append(input('Enter RB1: '))
            data[team].append(input('Enter RB2: '))
            data[team].append(input('Enter WR1: '))
            data[team].append(input('Enter WR2: '))


        conn = sq.connect("DGS-LLC.db")
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Manager(
            TEAM1ID integer,
            TEAM2ID integer,
            CURRENTROSTERID integer)''')

        count = 0
        for team in data:
            teamName = f'TEAM{count}ID'
            cur.execute(f'''CREATE TABLE IF NOT EXISTS {teamName}(
                ID integer,
                NAME string,
                QB1 string,
                QB2 string,
                RB1 string,
                RB2 string,
                WR1 string,
                WR2 string,
                WINS integer,
                LOSSES integer,
                TOTALPOINTS integer
            )''')

            sqlQuery = f"""INSERT INTO {teamName}(
                ID, NAME, QB1, QB2, RB1, RB2, WR1, WR2, WINS, LOSSES, TOTALPOINTS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            print(data[team])
            sqlContent = (randint(100000, 1000000), str(list(data.keys())[count]), data[team][0], data[team][1], data[team][2], data[team][3], data[team][4], data[team][5], 0, 0, 0)

            cur.execute(sqlQuery, sqlContent)

            count += 1


        cur.execute(f'''CREATE TABLE IF NOT EXISTS Roster(
            ID integer,
            {list(data.keys())[0]} integer,
            {list(data.keys())[1]} integer
            )''')
            
            # {list(data.keys())[2]} integer,
            # {list(data.keys())[3]} integer,
            # {list(data.keys())[4]} integer,
            # {list(data.keys())[5]} integer,
            # {list(data.keys())[6]} integer,
            # {list(data.keys())[7]} integer,

        cur.close()
        conn.close()
        

fill_teams(allData)