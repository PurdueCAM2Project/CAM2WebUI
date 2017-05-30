from django.utils import timezone
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pyvirtualdisplay import Display
from django.test import LiveServerTestCase

# test

# Create your tests here


class AddTestCase(LiveServerTestCase):


	def setUp(self):
		self.display = Display(visible=0, size=(800, 600))
		self.display.start()
		self.selenium = webdriver.Chrome()
		super(AddTestCase, self).setUp()

	def tearDown(self):
		self.selenium.quit()
		super(AddTestCase, self).tearDown()
		self.display.stop()

	def test_one(self):
		pass


		

