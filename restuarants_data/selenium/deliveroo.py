import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

class DeliverooScraper:
    def __init__(self, path):
        self.path = path
        self.website = 'https://deliveroo.co.uk/'
        self.options = webdriver.ChromeOptions()
        self.service = Service(self.path)
        self.driver = None
        self.postcode = None

    def start_driver(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.maximize_window()

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def accept_cookies(self):
        try:
            cookie = self.driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            cookie.click()
        except:
            pass

    def search_location(self, location):
        self.driver.get(self.website)
        time.sleep(2)
        self.accept_cookies()
        time.sleep(4)

        search_input = self.driver.find_element(By.ID, 'location-search')
        search_input.send_keys(location)

        search_button = self.driver.find_element(By.XPATH, '//*[@id="location-search-container"]/div/div/div/div[1]/div/div[2]/span/button')
        search_button.click()
        time.sleep(5)

    def click_terms(self):
        try:
            terms = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ccl-388f3fb1d79d6a36.ccl-6d2d597727bd7bab.ccl-59eced23a4d9e077.ccl-7be8185d0a980278')))
            terms.click()
        except:
            print('Cannot find the element to click')

    def sort_by_distance(self):
        dropdown = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[3]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/div/button')
        dropdown.click()
        time.sleep(2)

        sort_btn = self.driver.find_element(By.ID, 'distance-sidebar')
        sort_btn.click()
        time.sleep(5)

    def scroll_to_load_restaurants(self):
        scroll_pause_time = 2
        screen_height = self.driver.execute_script("return window.screen.height;")
        i = 1
        while True:
            self.driver.execute_script("window.scrollTo(0, {0});".format(screen_height * i))
            time.sleep(scroll_pause_time)
            i += 1
            if screen_height * i > 10000:
                break

    def extract_restaurants(self):
        restaurant_data = self.driver.find_elements(By.CLASS_NAME, 'HomeFeedUICard-cdbc09faf7465d96')
        restaurants = []
        for res_data in restaurant_data:
            postcode = self.postcode
            names = res_data.find_elements(By.CSS_SELECTOR, 'p.ccl-649204f2a8e630fd.ccl-a396bc55704a9c8a.ccl-ff5caa8a6f2b96d0.ccl-40ad99f7b47f3781')    # names[i].text.strip()
            restaurant_link = res_data.find_element(By.XPATH, './/a[@class="HomeFeedUICard-3e299003014c14f9"]').get_attribute('href')
             # Check if the restaurant is closed
            is_closed = bool(res_data.find_elements(By.XPATH, './/span[@class="HomeFeedUICard-96eca7a3375b9f17 HomeFeedUICard-b26ae8114c844f49"]/span'))

            for name in names:
                restaurant_name = name.text.strip()
            
            restaurants.append({
                'RESTAURANT POSTCODE': postcode,
                'RESTAURANT NAME': restaurant_name,
                'RESTUARANT LINK': restaurant_link,
                # 'IS OPEN': TODO
                'IS CLOSED': is_closed
            })
                    
        return restaurants

    def run(self, postcode):
        self.postcode = postcode
        self.start_driver()
        self.search_location(postcode)
        self.click_terms()
        time.sleep(5)
        self.sort_by_distance()
        self.scroll_to_load_restaurants()
        restaurants = self.extract_restaurants()
        self.close_driver()
        return pd.DataFrame(restaurants)

if __name__ == "__main__":
    path = '/home/kibet/Downloads/chromedriver'
    scraper = DeliverooScraper(path)
    postcode = 'NN16 9QY'
    df = scraper.run(postcode)
    df.to_csv('deliveroodata.csv', index=False)


# map_button="ccl-364e2ed6a76f91e9"