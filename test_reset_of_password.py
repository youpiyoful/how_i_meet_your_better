from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.auth.models import User
from django.core import mail


class MySeleniumTests(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    # def setUp(self):
    #     """
    #     init the db
    #     """
    #     self.register = {
    #         "first_name": "gabin",
    #         "last_name": "fornari",
    #         "username": "gabin@gmail.com",
    #         "email": "gabin@gmail.com",
    #         "password": "123",
    #     }
    #     User.objects.create_user(**self.register)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.register = {
            "first_name": "gabin",
            "last_name": "fornari",
            "username": "gabin@gmail.com",
            "email": "gabin@gmail.com",
            "password": "123",
        }
        User.objects.create_user(**cls.register)
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    def test_reset_of_password(self):
        """
        this method checks that a user
        can reset their password
        """
        self.selenium.get("%s%s" % (self.live_server_url, "/my-account/login"))
        link_to_password_reset = self.selenium.find_element_by_class_name('reset-password')
        link_to_password_reset.click()
        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('gabin@gmail.com')
        btn = self.selenium.find_element_by_css_selector('p + button')
        btn.click()
        self.assertIn(
            'Nous vous avons envoyé par courriel les instructions pour changer de mot de passe,',
            self.selenium.page_source
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(mail.outbox[0].body, "http://localhost:50461/users/reset/")
        print("coucou : ", mail.outbox[0].body)

        # self.selenium.get("%s%s" % (self.live_server_url, ""))
        
        



    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()