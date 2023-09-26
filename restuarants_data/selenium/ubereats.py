from operator import index
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)


class UberEatsScraper:
    def __init__(self, path):
        self.path = path
        self.website = "https://ubereats.com/"
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

    def select_from_list(self):
        country_link = self.driver.find_element(
            By.XPATH, '//*[@id="wrapper"]/div[3]/div[6]/div/div[2]/div[28]/a'
        )
        country_link.click()

    def select_location(self, location):
        try:
            self.driver.get(self.website)
            time.sleep(2)
            self.select_from_list()

            search_input = self.driver.find_element(
                By.ID, "location-typeahead-home-input"
            )
            search_input.send_keys(location)
            time.sleep(4)
            search_input.send_keys(Keys.ENTER)
        except:
            print("Cannot find the input element")

    def close_ads(self):
        try:
            ads = self.driver.find_element(
                By.XPATH, '//*[@id="main-content"]/div/div[1]/div[2]'
            )
            ads.click()
        except NoSuchElementException:
            print("no such ads")

    def sort_by_rating(self):
        # self.close_ads()
        checkbox = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="al l7 am dr cl l8"]/label[3]/div[2]')
            )
        )
        checkbox.click()

    def get_restaurant_names(self):
        restuarant_data = self.driver.find_elements(By.XPATH, '//div[@class="ak bl"]')
        restuarants = []
        for res_data in restuarant_data:
            postcode = self.postcode
            restuarant_names = res_data.find_element(
                By.XPATH, '//h3[@class="p0 ct ae ag"]'
            )

            # for name in restuarant_names:
            #     restuarant_name = name.text.strip()
            restuarants.append(
                {"POST CODE": postcode, "RESTUARANT NAME": restuarant_names}
            )
        return restuarants

    def run(self, postcode):
        self.postcode = postcode
        self.start_driver()
        time.sleep(2)
        self.select_location(postcode)
        time.sleep(5)
        self.sort_by_rating()
        time.sleep(5)
        restuarants = self.get_restaurant_names()
        time.sleep(5)
        self.close_driver()
        return pd.DataFrame(restuarants)


if __name__ == "__main__":
    path = "/home/kibet/Downloads/chromedriver"
    scraper = UberEatsScraper(path)
    postcode = "EC1N 8NX"
    df = scraper.run(postcode)
    df.to_csv("ubereats.csv", index=False)
