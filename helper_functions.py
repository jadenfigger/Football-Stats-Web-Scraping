from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setting selenium to headless mode, so that the browser wont open up during scraping process
cm = Options()
cm.add_argument("--headless")
DRIVER_PATH = 'C:\Miscellaneous\chromedriver_win32\chromedriver.exe'
WEEK = 2


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


def calculate_points(player_id, position, week):
    create_player_info(["AlleJo02"])