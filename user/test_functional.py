from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class MyUserSeleniumTests(StaticLiveServerTestCase):
    fixtures = ['all_data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/my-account/login'))
        username_input = self.selenium.find_element_by_name("email")

        username_input.send_keys('gabin@gmail.com')
        password_input = self.selenium.find_element_by_name("password_field")
        password_input.send_keys('123')
        # self.selenium.find_element_by_xpath('//input[@value="Connexion"]').click()
        submit_btn = self.selenium.find_element_by_id('submit-form')
        submit_btn.click()


    def test_create_account(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/my-account/register'))
        firstname_input = self.selenium.find_element_by_id("firstname")
        lastname_input = self.selenium.find_element_by_id("lastname")
        email_input = self.selenium.find_element_by_id('inputEmail1')
        password_input = self.selenium.find_element_by_id('inputPassword1')
        password_confirmation_input = self.selenium.find_element_by_id('inputPassword2')
        firstname_input.send_keys('Yoan')
        lastname_input.send_keys('Fornari')
        email_input.send_keys('yoan@gmail.com')
        password_input.send_keys('123')
        password_confirmation_input.send_keys('123')
        self.selenium.find_element_by_id('submit-form').click()
    

