from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

CHROME_DRIVER_PATH = 'C:/Development/chromedriver.exe'
COOKIE_URL = 'https://orteil.dashnet.org/cookieclicker/'
# OLD_COOKIE_URL = 'http://orteil.dashnet.org/experiments/cookie/'  # Classic version


class Gamer:

    def __init__(self):
        svc = Service(CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=svc)
        self.driver.maximize_window()
        self.driver.get(COOKIE_URL)
        self.cookie = None

    def load_game(self):
        """Opens the game's page in the browser and click through the unnecessary options."""
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.LINK_TEXT, "Got it!")))
        self.driver.find_element(By.LINK_TEXT, 'Got it!').click()
        self.driver.find_element(By.CSS_SELECTOR, '#promptContentChangeLanguage div.langSelectButton').click()
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.LINK_TEXT, "Don't show this again")))
        self.driver.find_element(By.LINK_TEXT, "Don't show this again").click()
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, 'bigCookie')))
        self.cookie = self.driver.find_element(By.ID, 'bigCookie')

    def mute_game(self):
        """Mutes the game's volume to avoid hearing constant clicking the entire time."""
        self.driver.find_element(By.ID, 'prefsButton').click()

        slider = self.driver.find_element(By.CSS_SELECTOR, '.sliderBox #volumeSlider')
        width = slider.size['width']

        move = ActionChains(self.driver)
        move.click_and_hold(slider).move_by_offset(-width, 0).release().perform()
        self.driver.find_element(By.CLASS_NAME, 'menuClose').click()

    def change_name(self, randomize_name, name):
        """Changes the name of the Cookie Bot if selected, otherwise click the "Randomize" button."""
        self.driver.find_element(By.CSS_SELECTOR, 'div#bakeryName.title').click()
        type_name = ActionChains(self.driver)

        if randomize_name or name == '':
            self.driver.find_element(By.CSS_SELECTOR, 'a#promptOption1.option').click()
        else:
            type_name.send_keys(name).perform()

        type_name.send_keys(Keys.ENTER).perform()

    def close_achievements(self):
        """Closes achievements if they pop up."""
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#notes .sidenote').click()
        except NoSuchElementException:
            pass

    def click_cookie(self, seconds):
        """Continuously clicks cookie for the specified amount of time per clicking loop, and also checks for golden
        cookies before and after loop time. """
        self.click_golden_cookie()

        click_now = time.time()
        click_stop_time = click_now + seconds
        while click_now < click_stop_time:
            self.cookie.click()
            click_now = time.time()

        self.click_golden_cookie()

    def click_golden_cookie(self):
        """Checks if a golden cookie is appearing on the screen and clicks it if exists."""
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#shimmers .shimmer').click()
        except NoSuchElementException:
            pass

    def buy_upgrade(self):
        """Buys an upgrade if you can afford it. Chooses the least expensive available upgrade."""
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#upgrades .enabled').click()
        except NoSuchElementException:
            pass

    def buy_items(self, item_limit):
        """Buys an item if you can afford it and if the currently owned number of items is under the specified limit.
        Limits to one purchase of each item type per clicking loop, if available, prioritizing the most expensive
        items first."""
        buyables = self.driver.find_elements(By.CSS_SELECTOR, '#products .enabled')[::-1]
        for item in buyables:
            try:
                count = item.find_element(By.CSS_SELECTOR, '.content .owned').text
                if count and int(count) >= item_limit:
                    buyables = [buyable for buyable in buyables if buyable != item]
            except NoSuchElementException:
                pass

        while buyables:
            top_item = buyables[0]
            top_item.click()
            time.sleep(0.1)
            buyables = [buyable for buyable in buyables if buyable != top_item]

    def pull_cps(self):
        """Returns the final Cookies Per Second after the total bot time has completed."""
        cps = self.driver.find_element(By.ID, 'cookiesPerSecond').text.split()[-1]
        return cps
