from django.utils import timezone
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import is_url_connectable

from pyvirtualdisplay import Display
from django.test import LiveServerTestCase

import os


# test

# Create your tests here


class AddTestCase(LiveServerTestCase):


	def setUp(self):
		#self.display = Display(visible=1, size=(1000, 1200))
		#self.display.start()
		self.selenium = webdriver.Chrome()
		super(AddTestCase, self).setUp()
		self.port = self.live_server_url.split(":")[2]
		self.username = os.environ['BASICAUTH_USERNAME']
		self.password = os.environ['BASICAUTH_PASSWORD']

		
	def tearDown(self):
		#self.selenium.quit()
		#super(AddTestCase, self).tearDown()
		#self.display.stop()
		return


	# test whether testcase works

	def test_one(self):
		pass


	# Test if page title is Cam2

	def test_mainpage_connection(self):
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/'
		browser.get(url)
		assert 'CAM²' in browser.title

	# test if login/register page title is Login	

	def test_login_page_connection(self):
		browser = self.selenium
		
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login'
		browser.get(url)
		assert 'Login' in browser.title

	def test_register_page_connection(self):
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/register'
		browser.get(url)
		assert 'Register' in browser.title
