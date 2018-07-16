from django.utils import timezone
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options


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
import time

# test

# Create your tests here


class AddTestCase(StaticLiveServerTestCase):
	"""Tests the functionality of the sites served by this Django app

	Contains several test cases to ensure that the site behaves as intended.

	Attributes:
		selenium: a testing environment based on a web browser driver
		port: the port of access used when testing using localhost as an address
		username: a username used to access the site, pulled from the environment
		password: a password used to access the site, pulled from the environment
		test_username: a generated username used to test certain functions of the site
		test_password: a generated password used to test certain functions of the site
	
	"""

	def setUp(self):
		"""Sets up the testing environment

		Sets up an environment that can be used to test the site by initializing the class attributes

		"""
		#self.display = Display(visible=0, size=(1000, 1200))
		#self.display.start()
		#d = DesiredCapabilities.CHROME
		#d['loggingPrefs'] = { 'browser':'ALL' }
		#self.selenium = webdriver.Chrome(desired_capabilities=d)
		options = Options()
		options.add_argument('--headless')
		time.sleep(10)
		self.selenium = webdriver.Firefox(options=options)
		User.objects.create_superuser(
			username='admin',
			password='admin',
			email='admin@example.com'
		)
		super(AddTestCase, self).setUp()
		self.port = self.live_server_url.split(":")[2]
		self.username = os.environ['BASICAUTH_USERNAME']
		self.password = os.environ['BASICAUTH_PASSWORD']
		self.test_username = ''.join(random.sample(string.ascii_uppercase + string.digits, 10))
		self.test_password = ''.join(random.sample(string.ascii_uppercase + string.digits, 10))


	def tearDown(self):
		"""Exits the testing environment and stops all testing

		Closes out of any testing systems.

		"""
		self.selenium.quit()
		super(AddTestCase, self).tearDown()
		# self.display.stop()
		return


	# test whether testcase works
	def test_a_one(self):
		print("start first test")
		pass
	
	def test_profile_admin(self):
		"""tests the functionality of the profile page and admin sign in

		Logs into the site as an admin and tests the functionality of the profile page.

		"""
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login/'
		browser.get(url)
		browser.implicitly_wait(10)
		un = browser.find_element_by_name('username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_name('submitbutton').click()
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"welcome"),
		        "the Continuous Analysis of Many CAMeras"
		    )
                )
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/profile/'
		browser.get(url)
		time.sleep(5)
		browser.find_element_by_name('appname').send_keys("apple")
		browser.find_element_by_name('add').click()
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"new_app"),
		        "apple"
		    )
		)

	# Test if page title is Cam2
	def test_connection(self):
		"""Tests several pages for correctness of title to ensure correct url routing

		Navigates to multiple pages and checks each one for a specific expected title

		"""
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/'
		browser.get(url)
		time.sleep(5)
		assert 'CAM²' in browser.title

		# test if login page title is Login

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login'
		browser.get(url)
		time.sleep(5)
		assert 'Login' in browser.title

		# test if register page title is Login

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/register'
		browser.get(url)
		time.sleep(5)
		assert 'Register' in browser.title


		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
		time.sleep(5)
		assert 'All Cameras' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/team'
		browser.get(url)
		time.sleep(5)
		assert 'Team' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/history'
		browser.get(url)
		time.sleep(5)
		assert 'History' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/email/contact'
		browser.get(url)
		time.sleep(5)
		assert 'Contact us' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/publications'
		browser.get(url)
		time.sleep(5)
		assert 'Publications' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset'
		browser.get(url)
		time.sleep(5)
		print(self.username, self.password)
		assert 'Forgot Password?' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset/complete'
		browser.get(url)
		time.sleep(5)
		assert 'Password Reset Completed' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset_email_sent'
		browser.get(url)
		time.sleep(5)
		assert 'Password Reset Email Sent' in browser.title


	def test_db_conneciton(self):
		"""Tests connecting to the Django database

		Attempts to connect to the Django database to test its functionality

		"""
		db_conn = connections['default']
		try:
		    c = db_conn.cursor()
		except OperationalError:
		    assert False
		else:
			pass


	# Test login and register locally. Generate long random strings for username and password, test if jump to redirect page

	def test_Login_Register_1(self):
		"""tests user registration and login

		First, tests registration of a new user. Then tests logging in and accessing the profile page.

		"""
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/register'
		browser.get(url)
		browser.implicitly_wait(90)
		frame = browser.find_element_by_tag_name('form')
		browser.switch_to.frame(frame)
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
		time.sleep(5)
		#Need email confirmation for suscessful login of test_username.
		#Therefore, use superuser to test login instead.
		x = browser.find_element_by_name('username') 
		#x.send_keys(self.test_username)
		x.send_keys('admin')
		y = browser.find_element_by_name('password')
		#y.send_keys(self.test_password)
		y.send_keys('admin')
		browser.find_element_by_name('submitbutton').click()
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"welcome"),
		        "the Continuous Analysis of Many CAMeras"
		    )
                )
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/profile/'
		browser.get(url)
		time.sleep(5)
		browser.find_element_by_name('appname').send_keys("apples")
		browser.find_element_by_name('add').click()
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"new_app"),
		        "apples"
		    )
		)
	def test_Login_Register_2(self):
		"""tests the system's response to a failed login

		Tries to login with a non-existent username and password and looks for a
		response indicating authentication failure

		"""		
		browser = self.selenium		
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/login'		

		browser.get(url)
		time.sleep(5)		
		x = browser.find_element_by_name('username')  # Find the search box		
		x.send_keys('wrongusername')
		y = browser.find_element_by_name('password')
		y.send_keys('wrongpassword')	
		browser.find_element_by_name('submitbutton').click()
		browser.implicitly_wait(10)
		
		error = browser.find_element(By.ID,value="loginerror")	
		
		assert error.get_attribute("innerHTML") == 'Please enter a correct username and password. Note that both fields may be case-sensitive.'		
		
		
	def test_Login_Register_3(self):
		"""Tests the system's response to mismatched passwords on registration

		Attempts to register a new user, but alters the password given in the confirm password field,
		then checks for an error response

		"""		
		browser = self.selenium		
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/register'		
		browser.get(url)		
		time.sleep(5)
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
		cp.send_keys(self.test_password + '123')

		browser.find_element_by_name('registerbutton').click()
		
		error = browser.find_element(By.ID,value="registererror")
		
		assert error.get_attribute("innerHTML") == 'The two password fields didn\'t match.'



	def test_Login_Register_4(self):
		"""Tests the error handling for registration with an invalid email address

		Attempts to register a user using an email address that does not match
		a correct pattern, then checks for the correct error response

		"""
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/register'
		browser.get(url)
		time.sleep(5)
		un = browser.find_element_by_name('username')
		un.send_keys(self.test_username)

		fn = browser.find_element_by_name('first_name')
		fn.send_keys('Test')

		ln = browser.find_element_by_name('last_name')
		ln.send_keys('Case')

		email = browser.find_element_by_name('email')
		email.send_keys('test@case')


		p = browser.find_element_by_name('password1')
		cp = browser.find_element_by_name('password2')

		p.send_keys(self.test_password)
		cp.send_keys(self.test_password)

		browser.find_element_by_name('registerbutton').click()

		error = browser.find_element(By.ID,value="registererror")

		assert error.get_attribute("innerHTML") == 'Enter a valid email address.'



	def test_Login_Register_5(self):
		"""Tests to see if the system prevents multiple users registering with the same username

		Registers a new user, then attempts to register a user with the same username, and
		looks for an error response.

		"""
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/register'
		browser.get(url)
		time.sleep(5)
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

		browser.get(url)
		time.sleep(5)
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

		error = browser.find_element(By.ID,value="registererror")

		assert error.get_attribute("innerHTML") == 'A user with that username already exists.'


	def test_url_validate(self):
		"""Tests the URLValidator given by Django

		Attempts to validate multiple URLs and sees if URLValidator correctly validates them

		"""
		url = URLValidator()
		try:
			url('https://engineering.purdue.edu/HELPS/Publications/papers/2016CloudcomB.pdf')
			url('https://engineering.purdue.edu/HELPS/Publications/papers/2016IEEEHST1.pdf')
			url('https://engineering.purdue.edu/HELPS/Publications/papers/2016IEEEHSTNPD.pdf')
			url('https://engineering.purdue.edu/HELPS/Publications/papers/KohLuEI2016.pdf')
			url('https://engineering.purdue.edu/HELPS/Publications/papers/CCBD2015Kaseb.pdf')
		except ValidationError as e:
			print(e)
			assert False
      

	def test_camera_state(self):
		"""Tests the functionality of the state field on the camera page

		On the camera page, selects the US in the country field, 
		then checks that the state field lists at least 50 options.

		"""
		print("start usa state test")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
		time.sleep(5)
		browser.implicitly_wait(10)
		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='country']")
		country_options = element.find_elements_by_tag_name("option")
		for option in country_options:
			if (option.get_attribute("value") == "USA"):
				option.click()
				break
			#print("Value is: %s" % option.get_attribute("value"))

		browser.implicitly_wait(10)

		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='state']")
		state_options = element.find_elements_by_tag_name("option")
		assert (len(state_options) >= 50)


	def test_camera_state_city(self):
		"""Tests the list of cities available in the field on the camera page

		Tests the city field by checking the number of choices given for
		cities in Indiana.

		"""
		print("start usa state city test")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
		time.sleep(5)
		browser.implicitly_wait(5)
		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='country']")
		country_options = element.find_elements_by_tag_name("option")
		for option in country_options:
			if (option.get_attribute("value") == "USA"):
				option.click()
				break
			#print("Value is: %s" % option.get_attribute("value"))

		browser.implicitly_wait(10)

		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='state']")
		state_options = element.find_elements_by_tag_name("option")

		for option in state_options:
			if (option.get_attribute("value") == "IN"):
				option.click()

		browser.implicitly_wait(10)
		element = browser.find_element_by_xpath("//select[@id='city']")
		city_options = element.find_elements_by_tag_name("option")
		assert (len(city_options) >= 60)


	def test_camera_state_multiple_states(self):
		"""Tests querying multiple states in the camera page

		Selects two statws in the list of possible states and checks the number of available
		city options that can be selected with the two states chosen.

		"""
		print("start usa multiple states test")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
		time.sleep(5)
		browser.implicitly_wait(5)
		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='country']")
		country_options = element.find_elements_by_tag_name("option")
		for option in country_options:
			if (option.get_attribute("value") == "USA"):
				option.click()
				#break
			#print("Value is: %s" % option.get_attribute("value"))

		browser.implicitly_wait(10)

		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='state']")
		state_options = element.find_elements_by_tag_name("option")

		for option in state_options:
			if (option.get_attribute("value") == "IN" or option.get_attribute("value") == "CA"):
				option.click()

		browser.implicitly_wait(10)
		element = browser.find_element_by_xpath("//select[@id='city']")
		city_options = element.find_elements_by_tag_name("option")
		assert (len(city_options) >= 500)

	def test_camera_disable_state(self):
		"""Tests the list of states for a country that has no states

		In the camera page, queries a country with no states, checks the options within states,
		then checks to ensure that cities can still be selected, even when no states exist.

		"""
		print("start german no states with cities")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
		time.sleep(5)
		browser.implicitly_wait(5)
		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='country']")
		country_options = element.find_elements_by_tag_name("option")
		for option in country_options:
			if (option.get_attribute("value") == "DE"):
				option.click()
				break
			#print("Value is: %s" % option.get_attribute("value"))

		browser.implicitly_wait(10)

		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='state']")
		state_options = element.find_elements_by_tag_name("option")

		#print(len(state_options))
		assert type(state_options) is list

		element = browser.find_element_by_xpath("//select[@id='city']")
		city_options = element.find_elements_by_tag_name("option")
		assert (len(city_options) >= 3000)


	def test_camera_disable_city(self):
		"""Checks the functions of a city list for countries with states

		On the camera page, queries for USA, then checks that no cities are listed
		when no states are queried.

		"""
		print("start usa no state with city test")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
		time.sleep(5)
		browser.implicitly_wait(5)
		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='country']")
		country_options = element.find_elements_by_tag_name("option")
		for option in country_options:
			if (option.get_attribute("value") == "USA"):
				option.click()
			#print("Value is: %s" % option.get_attribute("value"))

		browser.implicitly_wait(10)

		#element = browser.find_element_by_xpath("//div[@id='mapCanvas']/div/div/div")
		element = browser.find_element_by_xpath("//select[@id='city']")
		city_options = element.find_elements_by_tag_name("option")
		assert len(city_options) == 0
		
	
	def test_Login_Register_6(self):
		"""Tests the functionality of the Django admin databases for History and Leaders

		Signs into the Django admin interface, then enters the History and Leaders databases
		and tests their validations and error handling when given invalid inputs.

		"""
		#log in the admin account
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/admin/'
		browser.get(url)
		time.sleep(5)
		un = browser.find_element_by_name('username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div[@id='content-main']/form[@id='login-form']/div[@class='submit-row']/input[@value='Log in']").click()
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"site-name"),
		        "Django administration"
		    )
                )
		currentUrl = browser.current_url
		#Test the validation for history
		browser.find_element_by_xpath("//div[@id='container']/div[2]/div[@id='content-main']//tbody/tr[@class='model-history']/td").click()
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"content"),
		        "Add history"
		    )
                )
		browser.find_element_by_name('month').send_keys("13")
		browser.find_element_by_name('year').send_keys("2019")
		browser.find_element_by_name('_save').click()
		error1 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[1]/ul/li")
		error2 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[2]/ul/li")
		assert error1.get_attribute("innerHTML") == 'The maximum value is 12'
		assert error2.get_attribute("innerHTML") == 'The maximum value is 2017'
		#Test the validation for leader
		browser.get(currentUrl)
		WebDriverWait(browser, 10).until(
		    EC.text_to_be_present_in_element(
			(By.ID,"content"),
		        "Site administration"
		    )
                )
		browser.find_element_by_xpath("//div[@id='container']/div[2]/div[@id='content-main']//tbody/tr[@class='model-leader']/td").click()
		browser.find_element_by_name('leaderimg').send_keys("a.com")
		browser.find_element_by_name('leadername').send_keys("Harvey K. J")
		browser.find_element_by_name('leaderpagelink').send_keys("abcd???")
		browser.find_element_by_name('_save').click()
		error3 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[1]/ul/li")
		error4 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[3]/ul/li")
		error5 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[4]/ul/li")
		assert error3.get_attribute("innerHTML") == 'Invalid URL for this field'

	def test_forgot_password(self):
		"""Tests the functionality of the password reset page

		Attempts a password reset by entering an email and waiting for a response page confirming the sent email address.

		"""
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset'
		browser.get(url)
		time.sleep(5)
		email = browser.find_element_by_name('email')
		email.send_keys('test@case.net')  # input email
		browser.find_element_by_name('submitEmail').click()

		WebDriverWait(browser, 10).until(
			EC.text_to_be_present_in_element(
				(By.ID, 'EmailSent'),
				'Password reset email sent'
			)
		)
'''
	def test_admin_emailing(self):
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/admin/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div[@id='content-main']/form[@id='login-form']/div[@class='submit-row']/input[@value='Log in']").click()
		browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div[@id='content-main']/div[@class='app-auth module']/tbody/tr[@class='model-user']/th").click()
		#select users
		browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div[@id='content-main']/div[@id='changelist']/form[@id='changelist-form']/div[@class='results']/tbody/tr[@class='row1']/td/input[@class='action-select']").click()
		browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div[@id='content-main']/div[@id='changelist']/form[@id='changelist-form']/div[@class='actions']/select/option[@value='email_users']").click()
		browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div[@id='content-main']/div[@id='changelist']/form[@id='changelist-form']/div[@class='actions']/button").click()
		
		
	'''
