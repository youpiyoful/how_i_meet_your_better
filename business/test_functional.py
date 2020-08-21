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



# from time import sleep
# #import tempfile

# from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver import DesiredCapabilities
# from selenium.webdriver import FirefoxOptions
# from selenium.webdriver import FirefoxProfile

# capabilities = DesiredCapabilities.FIREFOX.copy()
# capabilities['browserName'] = 'firefox'
# capabilities['acceptInsecureCerts'] = False
# capabilities['marionette'] = True

# binary = FirefoxBinary('/mnt/c/Program Files/Mozilla Firefox/firefox.exe')
# profile = FirefoxProfile('/mnt/c/Users/yoanf/AppData/Roaming/Mozilla/Firefox/Profiles/1tz7ljhm.default')
# options = FirefoxOptions()


# # profile = tempfile.mkdtemp('.selenium')
# # print("*** Using profile: {}".format(profile))
# def run_test():
#     # options.headless = True
#     options.log.level = "trace"
#     options.profile = profile
#     options.binary = binary

#     driver = webdriver.Firefox(
#         options=options,
#         capabilities=capabilities,
#         executable_path="/mnt/c/WebDriver/bin/geckodriver.exe",)
#         service_args=["--marionette-port", "2828"])

#     driver.get('www.selenium.com')
#     sleep(5)
#     driver.close()


# if __name__ == "__main__":
#     run_test()
