from selenium import webdriver
import datetime as dt
from webdriver_auto_update import check_driver
from pathlib import Path
from scrap_functions import zpower_login,get_event_page_info, get_event_data

# Zwift credentials
username = 'ppalamarchuk87@gmail.com'
password = 'tr0t5kyvgn'

## Make sure to pass in the folder used for storing/downloading chromedriver
check_driver('C:/Users/USUARIO/Documents/Proyectos/zwift_racing_scrap')
driver = webdriver.Chrome("chromedriver")

event_info = []

zpower_login(username, password, driver)
event_data, driver = get_event_page_info(event_info, driver)
event_results, event_elevations = get_event_data(driver,event_data,zid='zid')
driver.quit()

# Para hacer: Hay que llevarlo a una base SQL
event_results.to_csv(Path('data',f'zpwr_events_results_{dt.date.today()}.csv'))
event_info = event_data.merge(event_elevations.reset_index(drop=True), how='left', on='zid')
event_info.to_csv(Path('data',f'zpwr_events_info_{dt.date.today()}.csv'))


## Fecha
#//*[@id="EVENT_DATE"]
