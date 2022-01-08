from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import time
import csv


class PieceFinder:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def extract(self, file: csv):
        """Use info from file to get the necessary information to use add to cart."""
        opened = open(file)
        opened_list = list(csv.reader(opened))
        i = 1

        while i < len(opened_list) + 1:
            self.driver.get("https://www.bricklink.com/v2/main.page")
            if i == 1:
                # click "accept" on the annoying cookie window
                html = "/html/body/div[6]/div/section/div/div[2]/div/section[1]/div[2]/div/button[2]"
                self.driver.find_element(By.XPATH, html).click()
            # ignore the first list, and start at [1][0]
            # the element index = 1
            # quantity index = 2
            # colour index = 3
            element = opened_list[i][1]
            quantity = opened_list[i][2]
            colour = opened_list[i][3]
            self.add_to_cart(element, quantity, colour)
            i += 1

    def add_to_cart(self, ele: str, qua: str, col: str):
        """Using extracted information, add a piece to the cart"""

        # finds the search bar
        search = self.driver.find_element(By.NAME, "nav-search")
        # types the piece element into the search bar
        search.send_keys(ele)
        # clicks the enter button
        search.send_keys(Keys.RETURN)

        # waits, then clicks the piece link
        self.driver.implicitly_wait(5)
        html = "/html/body/div[3]/center/table/tbody/tr/td/section/div/div/div[7]/div[1]/table/tbody/tr[2]/td[3]/a"
        self.driver.find_element(By.XPATH, html).click()

        # clicks the colour (black in this case)
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.LINK_TEXT, col).click()

        # click the dropdowns, select "new" and "canada", check "no min purchase", search
        self.driver.implicitly_wait(5)
        drop = Select(self.driver.find_element(By.XPATH, '//*[@id="_idSelCond"]'))
        drop.select_by_visible_text("New")
        drop2 = Select(self.driver.find_element(By.XPATH, '//*[@id="_idSelShipsTo"]'))
        drop2.select_by_visible_text("Canada")
        self.driver.find_element(By.XPATH, '//*[@id="_idchkNMP"]').click()
        self.driver.find_element(By.XPATH, '//*[@id="_idbtnSearch"]').click()

        # scroll, wait, then click "view"
        self.driver.implicitly_wait(5)
        self.driver.execute_script("window.scrollTo(0,1000)")
        time.sleep(3)
        html2 = "/html/body/div[3]/center/table/tbody/tr/td/section/div/div/div[1]/div[3]/table/tbody/tr[3]/td[5]/input"
        self.driver.find_element(By.XPATH, html2).click()

        # specify the quantity, add the item to the cart
        time.sleep(1)
        try:
            html3 = '/html/body/div[2]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div[3]/article/div[4]/div[2]/span/input'
            quantity = self.driver.find_element(By.XPATH, html3)
            quantity.send_keys(qua)
        except:
            html3 = '/html/body/div[2]/div[3]/div/div[3]/div[2]/div[2]/div[3]/div[3]/article/div[4]/div[2]/span/input'
            quantity = self.driver.find_element(By.XPATH, html3)
            quantity.send_keys(qua)

        self.driver.find_element(By.CSS_SELECTOR, '.bl-btn.primaryGreen.float-right').click()


if __name__ == "__main__":
    p = PieceFinder()
    p.extract('Brickset-inventory-10221-1.csv')

