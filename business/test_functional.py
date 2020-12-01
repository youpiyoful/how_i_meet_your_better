from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import reverse
from himyb.settings.base import BASE_DIR
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver

# from selenium.webdriver.support.wait import WebDriverWait

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True


class MyBusinessSeleniumTests(StaticLiveServerTestCase):
    fixtures = ["all_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(log_path="geckodriver.log", options=firefox_options)
        cls.selenium.implicitly_wait(10)
        print("wait 10 sec")

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_search_food(self):
        # timeout = 2
        self.selenium.get("%s%s" % (self.live_server_url, reverse("index")))
        # WebDriverWait(self.selenium, timeout).until(
        #     lambda driver: driver.find_element_by_tag_name('body'))
        input_search = self.selenium.find_element_by_id("product_name")
        input_search.send_keys("Acras de morue")
        self.selenium.find_element_by_xpath('//button[@value="Chercher"]').click()
        # input_search.click()


######################################
# from selenium import webdriver
# import time

# browser = webdriver.Firefox()
# time.sleep(10)
# browser.get('http://www.univ-orleans.fr')
# assert 'Université' in browser.title

# elem = browser.find_element_by_id('banniere')
# assert(elem is not None)

# browser.quit()
