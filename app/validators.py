from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.core.validators import MaxValueValidator
import re
from datetime import datetime

def validateURL (value):
	"""Checks a value and determines if it is valid as a URL

	Uses Django's URLValidator to determine if the given string's regex
	matches a pattern expected of a URL. Does not check for the existence
	of the page or file pointed to.

	Args:
		value: a string to be validated as a URL

	Returns:
		value, if it was a valid URL

	Raises:
		ValidationError: value does not match a valid URL pattern
	
	"""
	url_validator = URLValidator()
	try:
		url_validator(value)
	except:
		raise ValidationError("Invalid URL for this field")
	return value

def validateEmail (value):
	"""Checks a value and determines if it is valid as an email address

	Uses Django's validate_email() to determine if the given string's regex
	matches a pattern expected of an email address. Does not check for the existence
	of the address or of the domain.

	Args:
		value: a string to be validated as an email address

	Returns:
		value, if it was a valid email address

	Raises:
		ValidationError: value does not match a valid email address pattern
	
	"""
	try:
		validate_email(value)
	except:
		raise ValidationError("Wrong email form for this field")
	return value

def validateMonth (value):
	"""Checks a value and determines if it is valid as a month

	Uses a simple check to determine if the value given is valid as a month

	Args:
		value: a string to be validated as a month

	Returns:
		value, if it was a valid month

	Raises:
		ValidationError: value is too big to be a month of the year
	
	"""
	if value > 12:
		raise ValidationError("The maximum value is 12")
	return value

def validateYear (value):
	"""Checks a value and determines if it is valid as a year

	Uses a simple check to determine if the given year is valid for a date in the past

	Args:
		value: a string to be validated as a year

	Returns:
		value, if it was a valid year

	Raises:
		ValidationError: value is larger than the current year
	
	"""
	currentYear = datetime.now().year
	if value > currentYear:
		raise ValidationError("The maximum value is {}".format(currentYear))
	return value

def validateName (value):
	"""Checks a value and determines if it is valid as a full name

	Uses regular expressions to match a full name formatted as follows:
		A first name and last name (ex. Alice Carver)
		A first, middle, and last name (ex. Alice Bethany Carver)
		A first name, middle initial, and last name (ex. Alice B. Carver)

	Args:
		value: a string to be validated as a full name

	Returns:
		value, if it was a valid full name

	Raises:
		ValidationError: value does not match a valid full name pattern
	
	"""
	#if not re.match(r'^[\d\w\s\C\W]+$', value):
	if not re.match(r'[A-Z][a-z\-]+\s[A-Z][a-z\-]+$', value):	
		if not re.match(r'[A-Z][a-z\-]+\s[A-Z][a-z\.]+\s[A-Z][a-z\-]+$', value):
			raise ValidationError("Wrong form for this field")

	return value
	



		
