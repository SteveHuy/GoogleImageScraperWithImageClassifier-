import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def findPhotos(query1: str, query2: str):
    # Configure Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode, i.e., without a GUI


    # Create a new instance of ChromeDriver
    driver = webdriver.Chrome()


    # Navigate to Google Images
    driver.get("https://www.google.com/imghp")

    # Find the search bar and enter the query
    search_bar = driver.find_element(By.ID, "APjFqb")
    search_bar.send_keys(query1)
    search_bar.send_keys(Keys.ENTER)

    # Scroll down to load more images (adjust the value of 'scroll_count' as needed)
    scroll_count = 5
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Find all image elements
    image_elements = driver.find_elements(By.XPATH, "//img[@class='rg_i Q4LuWd']")

    # Create a directory to save the images
    save_directory = "data/query1"
    os.makedirs(save_directory, exist_ok=True)

    if len(os.listdir(save_directory)) != 0:
        remove_directory_contents(save_directory)
    

    # Download and save the images
    for index, image_element in enumerate(image_elements):
        image_url = image_element.get_attribute("src")
        if image_url is not None and image_url.startswith("http"):
            image_path = os.path.join(save_directory, f"{query1}_{index}.jpg")
            urllib.request.urlretrieve(image_url, image_path)
            print(f"Image {index + 1}/{len(image_elements)} downloaded and saved.")


    # Restart for second query
    driver.get("https://www.google.com/imghp")

    # Find the search bar and enter the query
    search_bar = driver.find_element(By.ID, "APjFqb")
    search_bar.send_keys(query2)
    search_bar.send_keys(Keys.ENTER)

    # Scroll down to load more images (adjust the value of 'scroll_count' as needed)
    scroll_count = 5
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Find all image elements
    image_elements = driver.find_elements(By.XPATH, "//img[@class='rg_i Q4LuWd']")

    # Create a directory to save the images
    save_directory = "data/query2"
    os.makedirs(save_directory, exist_ok=True)

    if len(os.listdir(save_directory)) != 0:
        remove_directory_contents(save_directory)

    # Download and save the images
    for index, image_element in enumerate(image_elements):
        image_url = image_element.get_attribute("src")
        if image_url is not None and image_url.startswith("http"):
            image_path = os.path.join(save_directory, f"{query2}_{index}.jpg")
            urllib.request.urlretrieve(image_url, image_path)
            print(f"Image {index + 1}/{len(image_elements)} downloaded and saved.")

    # Close the browser

    driver.quit()



def remove_directory_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove file

