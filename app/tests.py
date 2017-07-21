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


	# test whether testcase works
	def test_a_one(self):
		print("start first test")
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


		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
		assert 'Cameras' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/team'
		browser.get(url)
		assert 'Team' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/history'
		browser.get(url)
		assert 'History' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/email/contact'
		browser.get(url)
		assert 'Contact us' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/publications'
		browser.get(url)
		assert 'Publications' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset'
		browser.get(url)
		print(self.username, self.password)
		assert 'Forgot Password?' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset/complete'
		browser.get(url)
		assert 'Password Reset Completed' in browser.title

		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset_email_sent'
		browser.get(url)
		assert 'Password Reset Email Sent' in browser.title


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
		email.send_keys('test@case.net')


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



	def test_Login_Register_3(self):
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
		cp.send_keys(self.test_password + '123')

		browser.find_element_by_name('registerbutton').click()


		error = browser.find_element(By.ID,value="registererror")

		assert error.get_attribute("innerHTML") == 'The two password fields didn\'t match.'



	def test_Login_Register_4(self):
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
		email.send_keys('test@case')


		p = browser.find_element_by_name('password1')
		cp = browser.find_element_by_name('password2')

		p.send_keys(self.test_password)
		cp.send_keys(self.test_password)

		browser.find_element_by_name('registerbutton').click()

		error = browser.find_element(By.ID,value="registererror")

		assert error.get_attribute("innerHTML") == 'Enter a valid email address.'



	def test_Login_Register_5(self):
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

		error = browser.find_element(By.ID,value="registererror")

		assert error.get_attribute("innerHTML") == 'A user with that username already exists.'


	def test_url_validate(self):
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
		print("start usa state test")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
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
		print("start usa state city test")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
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
		print("start usa multiple states test")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
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
		print("start german no states with cities")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
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
		print("start usa no state with city test")
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/cameras'
		browser.get(url)
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
		#log in the admin account
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/admin/'
		browser.get(url)
		un = browser.find_element_by_name('username')
		un.send_keys("admin")
		pw = browser.find_element_by_name('password')
		pw.send_keys("admin")
		browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div[@id='content-main']/form[@id='login-form']/div[@class='submit-row']/input[@value='Log in']").click()
		currentUrl = browser.current_url
		#Test the validation for history
		browser.find_element_by_xpath("//div[@id='container']/div[2]/div[@id='content-main']//tbody/tr[@class='model-history']/td").click()
		browser.find_element_by_name('month').send_keys("13")
		browser.find_element_by_name('year').send_keys("2019")
		browser.find_element_by_name('_save').click()
		error1 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[1]/ul/li")
		error2 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[2]/ul/li")
		assert error1.get_attribute("innerHTML") == 'The maximum value is 12'
		assert error2.get_attribute("innerHTML") == 'The maximum value is 2017'
		#Test the validation for leader
		browser.get(currentUrl)
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
		browser = self.selenium
		url = 'http://' + self.username + ':' + self.password + '@localhost:' + self.port + '/password_reset'
		browser.get(url)

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
