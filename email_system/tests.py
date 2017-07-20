from telnetlib import EC
from webbrowser import browser
from selenium.webdriver.common.by import By
from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
import os
import random
import string
from django.contrib.auth.models import User

# Create your tests here.
from selenium.webdriver.support.wait import WebDriverWait


class AddTestCase(LiveServerTestCase):
    def setUp(self):
        #self.display = Display(visible=0, size=(1000, 1200))
        #self.display.start()
        self.selenium = webdriver.Firefox()
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
        super(AddTestCase, self).setUp()
        self.port = self.live_server_url.split(":")[2]
        self.username = os.environ['BASICAUTH_USERNAME']
        self.password = os.environ['BASICAUTH_PASSWORD']
        self.test_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.test_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def tearDown(self):
        self.selenium.quit()
        super(AddTestCase, self).tearDown()
        #self.display.stop()
        return

    def test_connection(self):
        browser = self.selenium

        url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset'
        browser.get(url)
        assert 'Forgot Password?' in browser.title

        url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset/complete'
        browser.get(url)
        assert 'Password Reset Completed' in browser.title

        url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset_email_sent'
        browser.get(url)
        assert 'Password Reset Email Sent' in browser.title

    def test_forgot_password(self):
        browser = self.selenium
        url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset'
        browser.get(url)

        email = browser.find_element_by_name('email')
        email.send_keys('test@case.net')#input email

        WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.ID, 'EmailSent'),
                'Email confirmation sent'
            )
        )


