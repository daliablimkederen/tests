import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import WebDriverWait

class TrelloBot(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=en')
        
        self.username = 'Dalka'
        self.password = 'passw0rd'
        self.email = 'dalia.blimke.deren@wp.pl'
        self.delay = 5
        self.driver = webdriver.Chrome(options = options)
        self.driver.implicitly_wait(self.delay)

    def tearDown(self):
        self.driver.quit()

    def test_navigate_to_registration_page(self):
        browser = self.driver
        browser.get('https://trello.com/signup')

        element = browser.find_element_by_id('email')
        element.clear()
        element.send_keys(self.email)
        element.send_keys(Keys.ENTER)

        email_url = browser.current_url
        
        wait = WebDriverWait(browser, self.delay)
        wait.until_not(ExpectedConditions.url_to_be(email_url))
        
        element = browser.find_element_by_xpath('//div[@id="signup-password"]/h1')
        self.assertTrue('Create a Trello Account' in element.text)

    def test_fail_to_create_an_account_by_using_existing_email(self):
        browser = self.driver
        browser.get('https://trello.com/signup?email=' + self.email)

        element = browser.find_element_by_id('email')
        element.clear()
        element.send_keys(self.email)

        element = browser.find_element_by_id('name')
        element.clear()
        element.send_keys(self.username)

        element = browser.find_element_by_id('password')
        element.clear()
        element.send_keys(self.password)
        element.send_keys(Keys.ENTER)

        wait = WebDriverWait(browser, self.delay)
        wait.until_not(ExpectedConditions.invisibility_of_element(browser.find_element_by_xpath('//div[@id="error"]')))

        element = browser.find_element_by_xpath('//div[@id="error"]/p')
        self.assertTrue('Email already in use' in element.text)

unittest.main()
