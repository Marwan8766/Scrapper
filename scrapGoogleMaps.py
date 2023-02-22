import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# define empty class to create objects from it
class Empty:
  pass

# define a list to store the places
places = []

# define a list to store the places links
links = []



# creating the driver

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# the following line is used when using selenium in server to not open a browser
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)



# fetch the link
driver.get("https://www.google.com/maps?hl=en")  

# find the search box element
searchBox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div/div[2]/form/input[1]"))) 
# write this value to the text box
searchBox.send_keys("tourist attractions in cairo")

# find the submit button for the searchBox
submit = driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div/div[2]/div[1]/button")

# submit the button
submit.click()


# find the elements that contains the data


# make the browser waits 5 sec till the page loads
# driver.implicitly_wait(5)

# scrollBtn =  driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]")

# find the scroll btn
scrollBtn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]"))) 

# define function to scroll the search results 
def infinite_scroll(driver):
    # number_of_elements_found = 0
    els = driver.find_elements(By.CLASS_NAME, 'TFQHme')
    timeout = time.time() + 5
    # loop while there is els element or the time is less than 5 sec
    while els and time.time() < timeout:
        try:
          # find all result elements
           els = driver.find_elements(By.CLASS_NAME, 'TFQHme') 
           
          #  wait 3 sec before scrolling
           driver.implicitly_wait(3)

           # scroll the results
           driver.execute_script("arguments[0].scrollIntoView();", els[-1])
           
          #  number_of_elements_found = len(els)
        except:
          els = driver.find_elements(By.CLASS_NAME, 'TFQHme')
          
           #  wait 3 sec before scrolling
          driver.implicitly_wait(3)
          
          driver.execute_script("arguments[0].scrollIntoView();", els[-1])
          # number_of_elements_found = len(els)

# call the function to scroll down the search results
infinite_scroll(driver)

# find all the search results anchors
touristAttractions = driver.find_elements(By.XPATH,"*//a[@class='hfpxzc']")

# loop over the attractions and print the name of the activity 
# for attraction in touristAttractions:
#     print(attraction.get_attribute("aria-label"))

# loop over the attractions and print the name of the activity 
for attraction in touristAttractions:
  # create a new object
  place = Empty()
  # create a field called name and set it to be the attraction name
  place.name = attraction.get_attribute("aria-label")
  # insert that object into the places array
  places.append(place)
  # insert the place link to the links array
  links.append(attraction.get_attribute("href"))


# loop over the links array 
i = 0
for link in links:
  if i == 3 :
    break
  driver.get(link)
  # find the rating 
  rating = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]/span/span[1]").text
  # find the type of the place
  placeType = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/span[1]/span[1]/button").text
  # find the overview
  overview = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[6]/button/div/div[1]/div[1]/span").text
  
  places[i].rating = rating
  places[i].placeType = placeType
  places[i].overview = overview
  i += 1


# make the browser open for 100 sec after executing the above code
time.sleep(100)

# close the browser
driver.quit()