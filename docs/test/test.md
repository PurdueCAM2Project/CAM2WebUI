# Django Selenium test

Selenium test environment is in the previous guide [Set up selenium test environment](https://purduecam2project.github.io/CAM2WebUI/selenium). If you haven't done that, click on the link and finish building up selenium environment first.

## Running Django Test

For every django app in the project, we can create a test for the app. Here in our project, visit CAM2WebUI/app folder and you can find file called tests.py. This is the file that we use to run testcase for "app" app. Go back to the main folder and run

```
python manage.py test app
```

You can run several testcases which are already created for the "app" app in the tests.py file.


## Setting up Liveserver testcases

Since we are going to create selenium test which needs to test in a live server environment, so we will use django LiveServerTestClass to create the project. 

```
from django.test import LiveServerTestCase
```

Then we create our test class with the parameter LiveServerTestCase

```
class AddTestCase(LiveServerTestCase):
```

Then we can create all the test cases within the addTestCase class.


## Setup and TearDown

For independent testcase, we all need to set up the browser driver and the display before the test and tear down them after the test, so django test have two created superclasses for us: setUp() and tearDown().

```
def setUp(self):
	self.display = Display(visible=0, size=(1000, 1200))
	self.display.start()
	self.selenium = webdriver.Chrome()
	super(AddTestCase, self).setUp()
```

To make the test run faster, everytime, we make the display visible=0. If there exists an error, then we can set the display visible=1. 

```
def tearDown(self):
	self.selenium.quit()
	super(AddTestCase, self).tearDown()
	self.display.stop()
	return
```

## Creating testcases

Now we can test the app by creating all the testcases. Note that all the test function should begin with "test_" and all the testcases run in alphabetical order. So if you would like to test the function in order, create test case name wisely.


```
def test_one(self):
	pass
```

This is our first testcase which only uses to test if test function works. 


## Webdriver API

You can use webdriver API to control your browser to direct to a particular url, to find element on a page or fill in a form etc. More details of web-driver API is on the page [Selenium Python Webdriver API](http://selenium-python.readthedocs.io/api.html)

The following are some our usages of web-driver API for testing

```
def test_connection(self):
	browser = self.selenium
	url = self.live_server_url
	browser.get(url)
	assert 'CAM²' in browser.title

```

In this case, we use web-driver to get the home page of the live server url. So in this testcase, we can test if the title of our homepage is CAM². If we can find our CAM² title, then that means we connect successfully to our server. 

Note that since our django app requires basic authentication, so our URL needs to become something like: "https://username:password@localhost:port/", so in our real test cases, we need to separate our self.live_server_url to allow username and password come into the URL string.

```
def test_connection(self):
	browser = self.selenium
	url = self.live_server_url
	browser.get(url)
	assert 'CAM²' in browser.title

```

```

def test_Login_Register_2(self):
	browser = self.selenium
	url = self.live_server_url + '/login'
	browser.get(url)
	x = browser.find_element_by_name('username')  # Find the search box
	x.send_keys('wrongusername')
	y = browser.find_element_by_name('password')
	y.send_keys('wrongpassword')
	browser.find_element_by_name('submitbutton').click()
	error = browser.find_element(By.ID,value="loginerror")
	assert error.get_attribute("innerHTML") == 'Please enter a correct username and password. Note that both fields may be case-sensitive.'

```

In this testcase, we first direct to the login page, and then we find the input box: username and password box and send text into the box. Then we click on the submitbutton of the browser by finding the element. Since the browser stays on the same page, we do not need to change our redirect url, we can just simply find the error mesage on the page. If we can see the error message, then that means our test cases pass!


```
def test_Login_Register_1(self):

....

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

....


```
This testcase is something different from the previous ones. Since after we click on the register button, we will direct to a new url automatically and may cost some time to direct to the new url. So we are going to use the above method. We will wait the browser for 10 seconds and wait to see if there exist an element which id called 'emailconfirm' on the page. If there exists an element, then the test pass. Else if the webpage cannot find the element called 'emailconfirm' on the page for more than 10 seconds, then we can assume that the testcase does not pass. 


***

That is almost everything for our testcases. If you would like to create more testcases, you can use [Selenium Python Webdriver API](http://selenium-python.readthedocs.io/api.html) as reference to test something new.


