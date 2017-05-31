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
		
	def tearDown(self):
		#self.selenium.quit()
		#super(AddTestCase, self).tearDown()
		#self.display.stop()
		return


	# test whether testcase works

	def test_one(self):
		pass


	# Test if page title is Cam2

	def test_title(self):
		browser = self.selenium
		port = self.live_server_url.split(":")[2]

		username = os.environ['BASICAUTH_USERNAME']
		password = os.environ['BASICAUTH_PASSWORD']

		url = 'http://' + username + ':' + password + '@localhost:' + port + '/'
		print(url)
		browser.get(url)
		
		assert 'CAM²' in browser.title
