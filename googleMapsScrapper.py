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
class Place:
    def __init__(self):
        self.name = ""
        self.link = ""
        self.rating = ""
        self.type = ""
        self.description = ""
        self.image = ""

    def __str__(self):
        return f"Name: {self.name}\nLink: {self.link}\nRating: {self.rating}\nType: {self.type}\nDescription: {self.description}\nImage:{self.image}"

# define a list to store the places
places = []

# define a list to store the places links
# links = []

# creating the driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# the following line is used when using selenium in server to not open a browser
# options.add_argument("--headless")

try:
    chrome_driver_path = r"E:\scrapper python\chromedriver.exe"
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # fetch the link
    driver.get("https://www.google.com/maps?hl=en")  
    # find the search box element
    searchBox = driver.find_element(By.ID, "searchboxinput")
    # write this value to the text box
    searchBox.send_keys("tourist attractions in cairo")
    # find the submit button for the searchBox
    submit = driver.find_element(By.ID, "searchbox-searchbutton")
    # submit the button
    submit.click()
    # find the scroll btn 
    scrollBtn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]"))) 
    # call the function to scroll down the search results
    infinite_scroll(driver,'TFQHme')
    # find all the search results anchors
    touristAttractions = driver.find_elements(By.CSS_SELECTOR,".Nv2PK.THOPZb.CpccDe")
    # loop over the search results anchors
    i = 0
    for attraction in touristAttractions:
      if i == 5:
        break
      i+=1
      # create a place object
      place = Place()
      # set its name field to be the attraction name
      place.name = attraction.get_attribute('aria-label')
      # find the anchor element inside the attraction div
      anchorElement = attraction.find_element(By.CLASS_NAME,"hfpxzc")
      # set the link field in place to be the link inside the anchor's href
      place.link = anchorElement.get_attribute('href')
      # # find the img elemnt that contains the image link
      # imgElement = attraction.find_element(By.CSS_SELECTOR,"img")
      # # set the image field to be the img link inside that img element src
      # place.image = imgElement.get_attribute('src') 
      # find the span element that contains the rate
      spanElement = attraction.find_element(By.CLASS_NAME,"MW4etd")
      # set the rating field to be the text inside this span
      place.rating = spanElement.text
      
      # print the place object
      print('*************************')
      print(place)
     

except Exception as e:
  print(f'Error Occured: {e}')


# make the browser open for 100 sec after executing the above code
time.sleep(100)

driver.quit()