# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxProfile
import time
# from selenium.webdriver import Chrome

binary = FirefoxBinary('/mnt/c/Program Files/Mozilla Firefox/firefox.exe')
profile = FirefoxProfile('/mnt/c/Users/yoanf/AppData/Roaming/Mozilla/Firefox/Profiles/1tz7ljhm.default')
cap = DesiredCapabilities().FIREFOX 
options = Options()
options.set_headless(headless=True)
# options.add_argument("--headless")
options.profile = profile
options.binary = binary
options.log.level = "trace"
cap["marionette"] = True
time.sleep(10)
browser = Firefox(
    # # firefox_binary=binary,
    capabilities=cap,
    executable_path="/opt/WebDriver/bin/geckodriver",
    # service_log_path='/home/youpiyoful/python_projet/himyb/user/Log/geckodriver.log',
    # log_path='/home/youpiyoful/python_projet/himyb/user/Log/',
    firefox_options=options,
    service_args=["--marionette-port", "2828"]
    # keep_alive=True
)



# class MySeleniumTests(StaticLiveServerTestCase):
#     fixtures = ['user-data.json']

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver(
#             capabilities=cap,
#             executable_path="/mnt/c/Users/yoanf/Desktop/gecko/geckodriver.exe",
#             firefox_options=options
#         )
#         cls.selenium.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def test_login(self):
#         self.selenium.get('%s%s' % (self.live_server_url, 'my-account/login'))
#         username_input = self.selenium.find_element_by_name("username")
#         username_input.send_keys('yoanfornari@gmail.com')
#         password_input = self.selenium.find_element_by_name("password")
#         password_input.send_keys('123')
#         self.selenium.find_element_by_xpath('//input[@value="Connexion"]').click()

# de l'app Django
# from selenium import webdriver

# browser = webdriver.Firefox()
browser.get('htpp:google.com')
# assert 'Pur Beurre' in browser.title

# browser.quit()
# # elem = browser.find_element_by_class_name('banniere')
# # assert(elem is not None)

browser.quit()



