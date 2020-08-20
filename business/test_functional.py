from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.shortcuts import reverse


class MyBusinessSeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_search_food(self):
        self.selenium.get('%s%s' % (self.live_server_url, reverse('index')))
        input_search = self.selenium.find_element_by_id('product_name')
        input_search.send_keys('Acras de morue')
        self.selenium.find_element_by_xpath('//button[@value="Chercher"]').click()
