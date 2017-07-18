from django.utils import timezone
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from pyvirtualdisplay import Display
from django.test import LiveServerTestCase

from django.db import connections
from django.db.utils import OperationalError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.test.testcases import LiveServerThread


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

import os
import base64
import uuid
import string
import random

# test

# Create your tests here


class AddTestCase(StaticLiveServerTestCase):


	def setUp(self):
		#self.display = Display(visible=0, size=(1000, 1200))
		#self.display.start()
		#d = DesiredCapabilities.CHROME
		#d['loggingPrefs'] = { 'browser':'ALL' }
		#self.selenium = webdriver.Chrome(desired_capabilities=d)
		self.selenium = webdriver.Chrome()
		User.objects.create_superuser(
			username='admin',
			password='admin',
			email='admin@example.com'
		)
		super(AddTestCase, self).setUp()
		self.port = self.live_server_url.split(":")[2]
		self.username = os.environ['BASICAUTH_USERNAME']
		self.password = os.environ['BASICAUTH_PASSWORD']
		self.test_username = "test_username"
		self.test_password = "test_password"


	def tearDown(self):
		self.selenium.quit()
		super(AddTestCase, self).tearDown()
		# self.display.stop()
		return


	# test whether testcase works
	def test_a_one(self):
		print("start first test")
		pass


	def test_profile_admin(self):
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_name('submitbutton').click()
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/profile/'
		browser.get(url)
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"Admin"),
		        "Admin Page"
		    )
		)
		browser.find_element_by_name('applist').send_keys("apple")
		browser.find_element_by_name('add').click()
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"new_app"),
		        "apple"
		    )
		)

		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/register'
		browser.get(url)

		un = browser.find_element_by_name('username')
		un.send_keys(self.test_username)

		fn = browser.find_element_by_name('first_name')
		fn.send_keys('Test')

		ln = browser.find_element_by_name('last_name')
		ln.send_keys('Case')

		email = browser.find_element_by_name('email')
		email.send_keys('test@case.net')


		p = browser.find_element_by_name('password1')
		cp = browser.find_element_by_name('password2')

		p.send_keys(self.test_password)
		cp.send_keys(self.test_password)

		browser.find_element_by_name('registerbutton').click()

		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
		        (By.ID, 'emailconfirm'),
		        'Email confirmation sent'
		    )
		)


		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login'

		browser.get(url)


		x = browser.find_element_by_name('username') 
		x.send_keys(self.test_username)
		y = browser.find_element_by_name('password')
		y.send_keys(self.test_password)
		browser.find_element_by_name('submitbutton').click()
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/profile/'
		browser.get(url)
		browser.find_element_by_name('applist').send_keys("apples")
		browser.find_element_by_name('add').click()
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"new_app"),
		        "apples"
		    )
		)














