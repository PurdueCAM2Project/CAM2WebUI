# Test the Validation of Administrator's Input
Allow admin to limit the inputs under the strict rules

## Set up the function for the validator
Create a validator function called `validator.py`

In `validator.py`:
```
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.core.validators import MaxValueValidator
import re
from datetime import datetime
```
We need to make use of the existing validator library for testing URL, Email and Year.

```
def validateURL (value):
	url_validator = URLValidator()
	try:
		url_validator(value)
	except:
		raise ValidationError("Invalid URL for this field")
	return value

def validateEmail (value):
	try:
		validate_email(value)
	except:
		raise ValidationError("Wrong email form for this field")
	return value

def validateYear (value):
	currentYear = datetime.now().year
	if value > currentYear:
		raise ValidationError("The maximum value is {}".format(currentYear))
	return value
```
If the according validation cannot pass, it will raise the Validation Error.
```

def validateMonth (value):
	if value > 12:
		raise ValidationError("The maximum value is 12")
	return value
    
def validateName (value):
	#if not re.match(r'^[\d\w\s\C\W]+$', value):
	if not re.match(r'[A-Z][a-z\-]+\s[A-Z][a-z\-]+$', value):	
		if not re.match(r'[A-Z][a-z\-]+\s[A-Z][a-z\.]+\s[A-Z][a-z\-]+$', value):
			raise ValidationError("Wrong form for this field")

	return value

```
For the test of year number, the value should be small than or equal to the recent number of year. For the test of name format, the name format allowed is very strict. The start letter of name should be Capital.

Now go to `models.py`. Import `validator.py`. Add the validator function to models. The following is an example.
```
teamimg = models.CharField(verbose_name='Team Image', max_length=300, validators=[validateURL])

```
To test the validator work after each updating in Github, use Selenium for web testing by adding testing function in `tests.py`.
```
	def test_Login_Register_6(self):
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
		assert error4.get_attribute("innerHTML") == 'Wrong form for this field'
		assert error5.get_attribute("innerHTML") == 'Invalid URL for this field'
		#Test the validation for member
		browser.get(currentUrl)
		browser.find_element_by_xpath("//div[@id='container']/div[2]/div[@id='content-main']//tbody/tr[@class='model-member']/td").click()
		browser.find_element_by_name('membername').send_keys("Harvey K. J")
		browser.find_element_by_name('memberimg').send_keys("a")
		browser.find_element_by_name('_save').click()
		error6 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[1]/ul/li")
		error7 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[2]/ul/li")
		assert error6.get_attribute("innerHTML") == 'Wrong form for this field'
		assert error7.get_attribute("innerHTML") == 'Invalid URL for this field'
		#Test the validation for publications
		browser.get(currentUrl)
		browser.find_element_by_xpath("//div[@id='container']/div[2]/div[@id='content-main']//tbody/tr[@class='model-publication']/td").click()
		browser.find_element_by_name('paperlink').send_keys("a")
		browser.find_element_by_name('_save').click()
		error8 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[2]/ul/li")
		assert error8.get_attribute("innerHTML") == 'Invalid URL for this field'
		#Test the validation for team
		browser.get(currentUrl)
		browser.find_element_by_xpath("//div[@id='container']/div[2]/div[@id='content-main']//tbody/tr[@class='model-team']/td").click()
		browser.find_element_by_name('teamimg').send_keys("a")
		browser.find_element_by_name('_save').click()
		error9 = browser.find_element_by_xpath("//div[@id='container']/div[@id='content']/div/form/div/fieldset/div[1]/ul/li")
		assert error9.get_attribute("innerHTML") == 'Invalid URL for this field'

```
This function use examples leading to errors. Every time after clicking the submit button, the validation error will pop out. The test functions will catch the error; If not, the testing function will stop immediately. 

