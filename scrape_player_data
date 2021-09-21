# Import scraping modules
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setting selenium to headless mode, so that the browser wont open up during scraping process
cm = Options()
cm.add_argument("--headless")
DRIVER_PATH = 'C:\Miscellaneous\chromedriver_win32\chromedriver.exe'
WEEK = 2

# nflTeamIds = ['buf', 'nwe', 'mia', 'nyj', 'cin', 'cle', 'pit', 'oti', 'htx', 'clt', 'jax', 'rai', 'den', 'kan', 'sdg', 'phi',
#               'was', 'dal', 'nyg', 'chi', 'min', 'gnb', 'det', 'car', 'tam', 'nor', 'atl', 'crd', 'ram', 'sea', 'sfo']
teamIds = ['crd']


# QB Index Lookup: Passing Yards = 8; touchdowns = 20; Rush Atempts = 16, Rush Yards = 17, 
QB_Lookup = {'PassYds': 8, 'Tds': 20, 'RushAtempts': 16, 'RushYds': 17}
# RB Index Lookup: Receptions = 11; Rec Yds = 12; Rush Atempts = 6; Rush Yards = 7; Touchdowns = 17
RB_Lookup = {'RushAtempts': 6, 'RushYds': 7, 'Rec': 11, 'RecYds': 12, 'Tds': 17}
# WB Index Lookup: Receptions = 7; Rec Yds = 8; Touchdowns = 14
WR_Lookup = {'Rec': 7, 'RecYds': 8, 'Tds': 14}

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


# allPIds = create_playerids(teamIds)
create_player_info(['MurrKy00'])

