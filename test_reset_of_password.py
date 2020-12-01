from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import reverse

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True


class MySeleniumTests(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    def setUp(self):
        """
        init the db
        """
        self.register = {
            "first_name": "gabin",
            "last_name": "fornari",
            "username": "gabin@gmail.com",
            "email": "gabin@gmail.com",
            "password": "123",
        }
        User.objects.create_user(**self.register)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(log_path='geckodriver.log', options=firefox_options)
        cls.selenium.implicitly_wait(10)

    def test_reset_of_password(self):
        """
        this method checks that a user
        can reset their password
        """
        url = reverse('user:login')
        self.selenium.get(self.live_server_url + url)
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
        print("body of mail : ", mail.outbox[0].body)
        self.assertIn("/users/reset/", mail.outbox[0].body)

        # self.selenium.get("%s%s" % (self.live_server_url, ""))

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()