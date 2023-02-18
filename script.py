import time
import re
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from alive_progress import alive_bar

from langdetect import detect

import argparse

options = Options()
parser = argparse.ArgumentParser()

parser.add_argument('plant_name')

args = parser.parse_args()

plant_name = args.plant_name  # "Salvia"
options.headless = True  # False
use_screenshot = False  # True
if use_screenshot:
    import keyboard

url = 'http://www.missouribotanicalgarden.org/PlantFinder/PlantFinderProfileResults.aspx?basic=' + plant_name

print("Plant:", plant_name)
print("Url:", url)


# Init driver
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=options)

driver.get(url)

result_wrapper = driver.find_element(By.CLASS_NAME, "results")
results = []

index = 1

for el in result_wrapper.find_elements(by=By.CSS_SELECTOR, value="a"):
    results.append({
        "name": el.text,
        "url": el.get_attribute("href")
    })
    print(str(index) + ": " + el.text)
    index += 1

input_index = 0

while True:
    try:
        input_index = int(input("Please select a plant: "))
    except:
        print("Prompt should be an integer")
    if input_index > 0 and input_index <= index - 1:
        break

plant = results[input_index - 1]

driver.get(plant["url"])

info_wrapper = driver.find_element(By.CLASS_NAME, "column-right")

for el in info_wrapper.find_elements(By.CSS_SELECTOR, "*"):
    if el.text and el.text != "Garden locations":
        print(el.text)


# Wait for the page to load

# try:
#     submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
#     print("Passed the cookie page")
#     submit_button.click()
# except:
#     print("Didn't have to pass the cookie page")

# print("Fetching places...")
# places = []

# feed = None
# for index, el in enumerate(driver.find_elements(By.CLASS_NAME, "DxyBCb")):
#     if "Résultats" in str(el.get_attribute("aria-label")):
#         feed = el
#         id = index

# # case 1 result only
# if feed == None:
#     print("There is only one place at this location.")
#     place = {
#         "name": driver.find_element(By.CLASS_NAME, "fontHeadlineLarge").text,
#         "url": driver.current_url
#     }
#     places.append(place)

# # case many results
# if feed != None:
#     print("There are many places at this location.")
#     reached_end = 0

#     try:
#         loader = feed.find_element(By.CLASS_NAME, "veYFef")

#         with alive_bar(120) as bar:
#             while (reached_end < 2):
#                 number_of_places = 0
#                 for el in driver.find_elements(By.CLASS_NAME, "hfpxzc"):
#                     if el.get_attribute("aria-label"):
#                         number_of_places += 1
#                         place = {
#                             "name": el.get_attribute("aria-label"),
#                             "url": el.get_attribute("href")
#                         }
#                         if number_of_places > len(places):
#                             places.append(place)

#                 bar(number_of_places - bar.current())

#                 try:
#                     feed.find_element(By.CLASS_NAME, "HlvSq")
#                     reached_end += 1
#                 except:
#                     loader_location_relative_to_screen_height = feed.size["height"] - \
#                         loader.location["y"]
#                     if loader_location_relative_to_screen_height == 53:
#                         while loader_location_relative_to_screen_height == 53:
#                             loader_location_relative_to_screen_height = feed.size["height"] - \
#                                 loader.location["y"]
#                             driver.execute_script(
#                                 "arguments[0].scrollTo(0,0)", feed)
#                     else:
#                         driver.execute_script(
#                             "arguments[0].scrollTo(0,arguments[0].scrollHeight)", feed)
#     except:
#         for el in driver.find_elements(By.CLASS_NAME, "hfpxzc"):
#             if el.get_attribute("aria-label"):
#                 place = {
#                     "name": el.get_attribute("aria-label"),
#                     "url": el.get_attribute("href")
#                 }
#                 places.append(place)

# print("Total number of places:", len(places))

# print("Fetching reviews with (" + str(stars_list) + " stars)...")

# reviews = []

# with alive_bar(max_reviews) as bar:
#     for place in places:
#         stop = False
#         driver.get(place["url"])
#         number = 0
#         for el in driver.find_elements(By.CLASS_NAME, "M77dve"):
#             if el.get_attribute("aria-label") != None:
#                 if "Plus d'avis" in str(el.get_attribute("aria-label")):
#                     ActionChains(driver).move_to_element(
#                         el).click(el).perform()
#                     time.sleep(2)
#                     for el2 in driver.find_elements(By.CLASS_NAME, "fontBodySmall"):
#                         try:
#                             if "avis" in str(el2.text):
#                                 number = int(re.sub(r'\D', '', str(el2.text)))
#                                 break
#                         except:
#                             pass

#                     # Get sidebar container element
#                     container = driver.find_elements(
#                         By.CLASS_NAME, "dS8AEf")[0]

#                     time.sleep(1)

#                     # Get and click sort button
#                     sort_button = container.find_elements(
#                         By.CLASS_NAME, "g88MCb")[-1]

#                     if sort_button.get_attribute("data-value") == "Trier":
#                         sort_button.click()
#                     else:
#                         hotel_button = container.find_elements(
#                             By.CLASS_NAME, "HQzyZ")[-1]
#                         hotel_button.click()

#                     time.sleep(2)

#                     # time.sleep(300)  # REFACTO

#                     # Get and sort sort by lowest rating button
#                     try:
#                         sort_by_lowest_rating_button = driver.find_elements(
#                             By.CLASS_NAME, "fxNQSd")[-1 if sort_by_lowest else -2]

#                         sort_by_lowest_rating_button.click()
#                     except:
#                         for i in range(0, 10):
#                             print("QUICK PRESS THE SORT BUTTON")
#                         time.sleep(2)

#                     time.sleep(2)

#                     loop = True

#                     # Number of reviews checked
#                     reviews_checked = 0

#                     while loop:
#                         if use_screenshot and keyboard.is_pressed("p"):
#                             print("Printed screen")
#                             driver.save_screenshot("screenshot.png")
#                         if reviews_checked >= 1000:
#                             break
#                         # List of the reviews elements
#                         results = driver.find_elements(By.CLASS_NAME, "jftiEf")

#                         tmp = 0

#                         loop2 = True

#                         # Expand all reviews
#                         while loop2:
#                             try:
#                                 driver.find_element(
#                                     By.CLASS_NAME, "w8nwRe").click()
#                             except:
#                                 break

#                         for review in results[reviews_checked:]:
#                             # Stop all if max_reviews is reached
#                             if len(reviews) >= max_reviews:
#                                 stop = True
#                                 loop = False
#                                 break

#                             tmp += 1

#                             # Content container
#                             content = review.find_elements(
#                                 By.CLASS_NAME, "GHT2ce")[1]

#                             # Review's stars
#                             stars = 0
#                             try:
#                                 star = content.find_element(
#                                     By.CLASS_NAME, "kvMYJc")
#                                 stars = int(star.get_attribute(
#                                     "aria-label").strip()[0])
#                             except:
#                                 stars = int(content.find_element(
#                                     By.CLASS_NAME, "fzvQIb").text[0])

#                             # Stop getting place reviews if star is above what we want
#                             if (stars > max(stars_list) if sort_by_lowest else stars < min(stars_list)):
#                                 loop = False
#                                 break

#                             # Review's text
#                             text = content.find_element(
#                                 By.CLASS_NAME, "wiI7pd").text

#                             if "(Traduit par Google)" in text:
#                                 if "(Avis d'origine)" in text:
#                                     text = text.split("(Avis d'origine)")[-1]
#                                 else:
#                                     text = text.split(
#                                         "(Traduit par Google)")[0]

#                             # Don't append if the review is from another language or if it's too short
#                             try:
#                                 if len(text) > 14 and stars in stars_list and detect(text) == lang:
#                                     reviews.append({
#                                         "name": place["name"],
#                                         "url": place["url"],
#                                         "text": text,
#                                         "stars": stars
#                                     })
#                                     bar()
#                             except:
#                                 pass

#                         reviews_checked += tmp

#                         # Stop loop once you get all the reviews from place
#                         if reviews_checked == number:
#                             loop = False

#                         # Scroll to the bottom of container
#                         driver.execute_script(
#                             "arguments[0].scrollTo(0,arguments[0].scrollHeight)", container)

#                     break

#         if stop:
#             break

#         with open('output/new/reviews_google_maps_' + company_name + '_' + location + '_' + lang + '.json', 'w') as file:
#             file.write(json.dumps(reviews, indent=2, ensure_ascii=False))


# with open('output/new/reviews_google_maps_' + company_name + '_' + location + '_' + lang + '.json', 'w') as file:
#     file.write(json.dumps(reviews, indent=2, ensure_ascii=False))

# Close the webdriver
driver.close()
