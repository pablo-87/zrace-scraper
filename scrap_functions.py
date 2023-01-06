from typing import Optional
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import json
import datetime as dt
from webdriver_auto_update import check_driver
from pathlib import Path

def zpower_login(username:str,password:str,driver):
    
    login_url = 'https://zwiftpower.com/ucp.php?mode=login&amp;login=external&amp;oauth_service=oauthzpsso'
    driver.get(login_url)
    driver.find_element(By.XPATH,'//*[@id="login"]/fieldset/div/div[1]/div/a').click()
    # Username
    driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(username)
    # Password
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)
    # submit login
    driver.find_element(By.XPATH,'//*[@id="submit-button"]').click()
    # filter for past results
    driver.find_element(By.XPATH,'//*[@id="button_event_results"]').click()
    # take last 7 day results and iterate across pages
    ## Filters
    driver.find_element(By.XPATH,'//*[@id="button_event_filter"]').click()
    """Button 2 for 1 day, 3 for 3 days and 4 for 7 days"""
    driver.find_element(By.XPATH,'//*[@id="filter_options"]/div/div[9]/button[2]').click()

def get_event_page_info(event_info:list,driver):
    '''
    event_info: an empty list to be filled
    driver: the web driver 
    '''
    # Init page
    WebDriverWait(driver,2)
    links_pg = driver.find_elements(By.CLASS_NAME,'no_under.hover_green')
    print('links getted')

    # Events ID (zid)
    events_pg_id = []

    for link in links_pg:
        events_pg_id.append(link.get_attribute('href').split("=")[1])

    # Event info
    print('retrieving event info')

    for event in events_pg_id:
        event_name = driver.find_element(By.XPATH,'//*[@id="'+event+'"]/td[3]')
        event_name = event_name.text
            
        distance = driver.find_element(By.XPATH,'//*[@id="'+event+'"]/td[5]')
        distance = distance.text.split(" ")[0]
            
        laps_time = driver.find_element(By.XPATH,'//*[@id="'+event+'"]/td[6]')
        laps_time = laps_time.text.split(" ")
            
        route_name = driver.find_element(By.XPATH,'//*[@id="'+event+'"]/td[7]')
        route_name = route_name.text
        """climbs = []
        for climb in range(1,5):
            try:
                route_climb = driver.find_element(By.XPATH,'//*[@id="'+event+'"]/td[8]/span/i['+str(climb)+']').get_attribute('title')
                    
            except:
                None
            climbs.append(route_climb)
        try:
            draft = driver.find_element(By.XPATH,'//*[@id="'+event+'"]/td[9]/div[1]/i[1]').get_attribute('title')
        except:
            None"""
            
        event_info.append([event, event_name, distance, laps_time, route_name])
    
    #prev_last_event_id = event

    driver.find_element(By.XPATH,'//*[@id="zwift_event_list_next"]/a').click()
    event_data = pd.DataFrame(event_info,
                          columns={'zid':1,
                                   'event_name':2,
                                   'distance':3,
                                   'laps_time':4,
                                   'zroute':5,
                                   #'climb':6,
                                   #'draft':7,
                                   }
                    ).reset_index(drop=True)
    return event_data, driver

def get_event_data(driver, event_data:pd.DataFrame,zid:str='zid'):
    # Results of events list
    print('retriving results')
    results = pd.DataFrame()
    for event_id in event_data[zid]:
        try:
            json_url = 'https://zwiftpower.com/cache3/results/'+ event_id +'_view.json' 
            driver.get(json_url)
            # take json as str
            json_content = driver.find_element(By.CSS_SELECTOR,'body > pre').text
            zui_df = pd.DataFrame.from_dict(json.loads(json_content)['data'])
            results = results.append(zui_df)
        except:
            print("Access denied: Event ID "+str(event_id))

    elevations = pd.DataFrame()
    for event in event_data[zid]:
        driver.get('https://zwiftpower.com/events.php?zid=' + event)
        try:
            elevation = driver.find_element(By.XPATH,'//*[@id="category_detail"]/div/span[5]/b[2]').text
        except:
            try:
                elevation = driver.find_element(By.XPATH,'//*[@id="category_detail"]/div/span[2]/b[2]').text
            except :
                try:
                    elevation = driver.find_element(By.XPATH,'//*[@id="category_detail"]/div/span[6]/b[2]').text
                except:
                    elevation = None
    
        aux = pd.DataFrame({zid: [event],
                        'elevation_gain' : [elevation]
                        })
        elevations = elevations.append(aux)
    return results, elevations