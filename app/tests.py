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

from django.db import connections
from django.db.utils import OperationalError

import os
import base64
import uuid

# test

# Create your tests here


class AddTestCase(LiveServerTestCase):


	def setUp(self):
		self.display = Display(visible=0, size=(1000, 1200))
		self.display.start()
		self.selenium = webdriver.Chrome()
		super(AddTestCase, self).setUp()
		self.port = self.live_server_url.split(":")[2]
		self.username = os.environ['BASICAUTH_USERNAME']
		self.password = os.environ['BASICAUTH_PASSWORD']
		self.test_username = str(uuid.uuid4())
		self.test_password = str(uuid.uuid4())

		
	def tearDown(self):
		self.selenium.quit()
		super(AddTestCase, self).tearDown()
		self.display.stop()
		return


	# test whether testcase works

	def test_one(self):
		pass


	# Test if page title is Cam2

	def test_connection(self):
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/'
		browser.get(url)
		assert 'CAM²' in browser.title

		# test if login page title is Login	

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login'
		browser.get(url)
		assert 'Login' in browser.title

		# test if register page title is Login	

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/register'
		browser.get(url)
		assert 'Register' in browser.title


	def test_db_conneciton(self):
		db_conn = connections['default']
		try:
		    c = db_conn.cursor()
		except OperationalError:
		    assert False
		else:
			pass


	# Test login and register locally. Generate long random strings for username and password, test if jump to redirect page

	def test_Login_Register_1(self):
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
		email.send_keys('agc123@yeah.net')


		p = browser.find_element_by_name('password1')
		cp = browser.find_element_by_name('password2')

		p.send_keys(self.test_password)
		cp.send_keys(self.test_password)

		browser.find_element_by_name('registerbutton').click()

		#test if register can work

		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
		        (By.ID, 'emailconfirm'),
		        'Email confirmation sent'
		    )
		)


		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login'

		browser.get(url)


		x = browser.find_element_by_name('username')  # Find the search box
		x.send_keys(self.test_username)
		y = browser.find_element_by_name('password')
		y.send_keys(self.test_password)
		browser.find_element_by_name('submitbutton').click()

		WebDriverWait(browser, 5).until(
		    EC.text_to_be_present_in_element(
		        (By.ID, 'someprofile'),
		        self.test_username + '\'s Profile'
		    )
		)


	def test_Login_Register_2(self):
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login'

		browser.get(url)
		x = browser.find_element_by_name('username')  # Find the search box
		x.send_keys('wrongusername')
		y = browser.find_element_by_name('password')
		y.send_keys('wrongpassword')
		browser.find_element_by_name('submitbutton').click()

		error = browser.find_element(By.ID,value="loginerror")

		assert error.get_attribute("innerHTML") == 'Please enter a correct username and password. Note that both fields may be case-sensitive.'

		

	




