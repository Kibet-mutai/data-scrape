import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DeliverooScraper:
    def __init__(self, path):
        self.path = path
        self.website = 'https://deliveroo.co.uk/'
        self.options = webdriver.ChromeOptions()
        self.service = Service(self.path)
        self.driver = None

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
        # restaurant_data = self.driver.find_elements(By.XPATH, '//li[@class="HomeFeedGrid-b0432362335be7af"]')
        restaurants = []
        names = self.driver.find_elements(By.XPATH, '//li[@class="HomeFeedUILines-8bd2eacc5b5ba98e"]/span/p')
        try:
            radius_elements = self.driver.find_elements(By.XPATH, '//li[@class="HomeFeedUILines-55cd19148e4c15d6"]/span/span[contains(@class, "ccl-649204f2a8e630fd")]')
        except:
            print("No element found!")

        for i in range(len(names)):
            restaurant_name = names[i].text.strip()
            # print(restaurant_name)
            radius = 'N/A'
            reviews = 'N/A'

            if i < len(radius_elements):
                radius_data = radius_elements[i].text.strip()
                # print(radius_data)
                radius_match = re.search(r'([\d.]+)\s*miles away', radius_data)
                if radius_match:
                    radius = radius_match.group(1)

            if any(word in radius_data for word in ['Good', 'Excellent', 'Bad']):
                reviews_match = re.search(r'(\d+\.\d+)\s*(Good|Excellent|Bad)', radius_data)
                if reviews_match:
                    reviews = reviews_match.group(1)
            restaurants.append({'RESTAURANT NAME': restaurant_name, 'RESTAURANT DELIVERY RADIUS': radius, 'RESTAURANT REVIEWS': reviews})
                
        return restaurants

    def run(self, location):
        self.start_driver()
        self.search_location(location)
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
    df = scraper.run('NN16 9QY')
    df.to_csv('deliverooptwt.csv', index=False)
