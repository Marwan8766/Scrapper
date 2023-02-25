import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrolling import infinite_scroll


class Place:
    def __init__(self):
        self.name = ""
        self.link = ""
        self.rating = ""
        self.type = ""
        self.description = ""
        self.image = ""
        self.open_close_times = {}

place = Place()

place.link = "https://www.google.com/maps/place/Masged+and+Madraset+Soltan+Hassn/@30.0328679,31.2562843,17z/data=!3m1!4b1!4m6!3m5!1s0x145840ac1c97a4f7:0x8412ca0f201c9352!8m2!3d30.0328679!4d31.2562843!16s%2Fg%2F12hm9lhq7?authuser=0&hl=en"

path =  r"E:\scrapper python\chromedriver.exe"


def fill_place_details(place,driver_path):
    """
    modifies the place object which is the parameter to add description, type, image, open close times to it.

    :param place: The place object which will be modified.
    :type place: object
    :param driver_path: The path of the chrome driver.
    :type driver_path: String

    """ 
    # creating the driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    try:
        # fetch the link
        driver.get(place.link)

        # find an element to make sure that the page has loaded before scrolling
        descriptionDiv = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "PYvSYb")))
    except:
        descriptionDiv = False  

    # scrolls the page
    # infinite_scroll(driver,'ipilje')

    if descriptionDiv:
        # find the span that contains description inside the description div
        descriptionSpan = descriptionDiv.find_element(By.CSS_SELECTOR,'span')
        # put the description inside description field
        place.description = descriptionDiv.text
    
    try:  
        # find the button containing the type
        typeBtn = driver.find_element(By.CLASS_NAME,'DkEaL')
        # set the type field to be the text inside the btn
        place.type = typeBtn.text
    except:
        place.type = ""  
    
    try:   
        # find the btn containing the img
        imgBtn = driver.find_element(By.CSS_SELECTOR,'.aoRNLd.kn2E5e.NMjTrf.lvtCsd')
    except:
        imgBtn = False  

    if imgBtn:  
        # find the img inside the image btn
        image = imgBtn.find_element(By.TAG_NAME,'img')
        # set the image field to be the img link inside the img
        place.image = image.get_attribute('src')

    # find the open close times
    try:
        
        try:
            # find the div that contains the code which shows the table
            showTableDiv = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.  CLASS_NAME, "OqCZI")))
        except:
            showTableDiv = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.  CLASS_NAME, "OyjIsf")))

        # will move the mouse cursor to the element and then perform a click on the element It  can be useful when you want to simulate more complex user interactions on the page
        ActionChains(driver).move_to_element(showTableDiv).click(showTableDiv).perform()

        # find open close times table
        open_close_table = driver.find_element(By.CSS_SELECTOR,'.eK4R0e.fontBodyMedium')

        # find all rows in the table
        open_close_table_rows = open_close_table.find_elements(By.CLASS_NAME,'y0skZc')
        # loop over the table rows
        for row in open_close_table_rows:
             # find the table data contains day inside the row
             day_table_data = WebDriverWait(row, 10).until(EC.presence_of_element_located ((By.     CLASS_NAME, 'ylH6lf')))
             # find all the div elemnts inside this td
             day_table_data_divs = day_table_data.find_elements(By.CSS_SELECTOR,'div')
             # get the text of the first to be the day 
             day = day_table_data_divs[0].text
             # define an array to store the times in it 
             times = []
             # find the open close times table data
             open_close_table_data = row.find_element(By.CLASS_NAME,'mxowUb')
             # find all the ordered lists inside this list
             open_close_ordered_lists = open_close_table_data.find_elements(By.CLASS_NAME, 'G8aQO')
             # loop over the ordered list to find open close times
             for open_close_time in open_close_ordered_lists:
               # find the time
               open_close = open_close_time.text.replace('\u202f',' ').split('?')
               open_close_text = open_close[0]

               if open_close_text != "Closed":   
                 time = open_close_text.split('–')
               else:
                time = "Closed"

               # add this list to times list
               times.append(time)
               place.open_close_times[day] = times
    except:
      place.open_close_times = {}







fill_place_details(place,path)

print(place.description)
print(place.type)
print(place.image)
print(place.open_close_times)
