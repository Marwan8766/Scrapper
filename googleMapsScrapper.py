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
        self.open_close_times = {}


    # def __str__(self):
    #     return f"Name: {self.name}\nLink: {self.link}\nRating: {self.rating}\nType: {self.type}\nDescription: {self.description}\nImage:{self.image}"


chrome_driver_path = r"E:\scrapper python\chromedriver.exe"
query = "restaurants in cairo"


def find_places_in_city(query,driver_path,placesLength=None):

  """
  Returns array of places objects found with each place name, link, rating.

  :param query: The query which will be put in the search box of google maps.
  :type query: String
  :param driver_path: The path of the chrome driver.
  :type driver_path: String
  :param placesLength: The length of the returned array of places objects.
  :type placesLength: int
  :returns: The array of places objects found.
  :rtype: array of objects
  """
 
  # define a list to store the places
  places = []

  # create a place object
  place = Place()

  # creating the driver
  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])

  # the following line is used when using selenium in server to not open a browser
  options.add_argument("--headless")

  try:
      
      driver = webdriver.Chrome(executable_path=driver_path, options=options)
      # fetch the link
      driver.get("https://www.google.com/maps?hl=en")  
      # find the search box element
      searchBox = driver.find_element(By.ID, "searchboxinput")
      # write this value to the text box
      searchBox.send_keys(query)
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

        if placesLength is not None:
          if i == placesLength:
           break
           i+=1

        # set its name field to be the attraction name
        place.name = attraction.get_attribute('aria-label')
        # find the anchor element inside the attraction div
        anchorElement = attraction.find_element(By.CLASS_NAME,"hfpxzc")
        # set the link field in place to be the link inside the anchor's href
        place.link = anchorElement.get_attribute('href')
        
        try:
          # find the span element that contains the rate
          spanElement = attraction.find_element(By.CLASS_NAME,"MW4etd")
        except:
          spanElement = False  
        # set the rating field to be the text inside this span
        if spanElement: place.rating = spanElement.text
        
        # # print the place object
        # print('*************************')
        # print(place)
        print(place.name)
        print(place.link)
        print(place.rating)
        places.append(place)
      
      return places
  except Exception as e:
    print(f'Error Occured: {e}')


# make the browser open for 100 sec after executing the above code
# time.sleep(100)

# driver.quit()


find_places_in_city(query,chrome_driver_path)