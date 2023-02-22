import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# define function to scroll the search results 
def infinite_scroll(driver,className):
    els = driver.find_elements(By.CLASS_NAME, className)
    timeout = time.time() + 7
    while els and time.time() < timeout:
        try:
            els = driver.find_elements(By.CLASS_NAME, className) 
            driver.implicitly_wait(3)
            driver.execute_script("arguments[0].scrollIntoView();", els[-1])
        except:
            els = driver.find_elements(By.CLASS_NAME, className)
            driver.implicitly_wait(3)
            driver.execute_script("arguments[0].scrollIntoView();", els[-1])