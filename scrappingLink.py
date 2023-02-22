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
# define empty class to create objects from it
# class Empty:
#     pass
# class Place:
#     def __init__(self):
#         self.name = ""
#         self.link = ""
#         self.rating = ""
#         self.type = ""
#         self.description = ""
#         self.image = ""

#     def __str__(self):
#         return f"Name: {self.name}\nLink: {self.link}\nRating: {self.rating}\nType: {self.type}\nDescription: {self.description}\nImage:{self.image}"


class Place:
    def __init__(self):
        self.name = ""
        self.link = ""
        self.rating = ""
        self.type = ""
        self.description = ""
        self.image = ""
        self.open_close_times = {}
# define a list to store the places links
# links = []
place = Place()
# creating the driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
# fetch the link
driver.get("https://www.google.com/maps/place/Cairo+Tower/data=!4m7!3m6!1s0x1458409aa81d58a5:0x6ce6bf7cd258d6fe!8m2!3d30.045915!4d31.2242898!16zL20vMDVqN3lu!19sChIJpVgdqJpAWBQR_tZY0ny_5mw?authuser=0&hl=en&rclk=1") 

# find an element to make sure that the page has loaded before scrolling
descriptionDiv = descriptionDiv = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "PYvSYb")))

# scrolls the page
# infinite_scroll(driver,'ipilje')

# find the span that contains description inside the description div
descriptionSpan = descriptionDiv.find_element(By.CSS_SELECTOR,'span')
# put the description inside description field
place.description = descriptionDiv.text
# find the button containing the type
typeBtn = driver.find_element(By.CLASS_NAME,'DkEaL')
# set the type field to be the text inside the btn
place.type = typeBtn.text
# find the btn containing the img
imgBtn = driver.find_element(By.CSS_SELECTOR,'.aoRNLd.kn2E5e.NMjTrf.lvtCsd')
# find the img inside the image btn
image = imgBtn.find_element(By.TAG_NAME,'img')
# set the image field to be the img link inside the img
place.image = image.get_attribute('src')




# find the open close times

# find the div that contains the code which shows the table
showTableDiv = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "OqCZI")))


# will move the mouse cursor to the element and then perform a click on the element It can be useful when you want to simulate more complex user interactions on the page
ActionChains(driver).move_to_element(showTableDiv).click(showTableDiv).perform()

# find open close times table
open_close_table = driver.find_element(By.CSS_SELECTOR,'.eK4R0e.fontBodyMedium')
# driver.execute_script("arguments[0].style.display = 'block';", open_close_table)

# find all rows in the table
open_close_table_rows = open_close_table.find_elements(By.CLASS_NAME,'y0skZc')
# loop over the table rows
for row in open_close_table_rows:
  # find the table data contains day inside the row
  day_table_data = WebDriverWait(row, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ylH6lf')))
  # find all the div elemnts inside this td
  day_table_data_divs = day_table_data.find_elements(By.CSS_SELECTOR,'div')
  # get the text of the first to be the day 
  day = day_table_data_divs[0].text
  print(day)
  # define an array to store the times in it 
  times = []
  # find the open close times table data
  open_close_table_data = row.find_element(By.CLASS_NAME,'mxowUb')
  # find the open close times unordered list
  # open_close_unordered_list = open_close_table_data.find_element(By.CLASS_NAME,'fontTitleSmall')
  # find all the ordered lists inside this list
  open_close_ordered_lists = open_close_table_data.find_elements(By.CLASS_NAME,'G8aQO')
  # loop over the ordered list to find open close times
  for open_close_time in open_close_ordered_lists:
    # define the array that will store the open close time
    time = []
    # find the time
    open_close = open_close_time.text.replace('\u202f',' ').split('?')
    print(open_close)
    openTime = open_close[0] + ' ' + open_close[1]
    closeTime = open_close[2] + ' ' + open_close[3]
    openTimeList = [openTime]
    closeTimeList = [closeTime]
    # add this time to time list
    time.append(openTime).append(closeTime)
    # add this list to times list
    times.append(time)
    print(times)
    

print(place.description)
print(place.type)
print(place.image)
# print(place.open_close_times['Monday'])
print(place.open_close_times)







