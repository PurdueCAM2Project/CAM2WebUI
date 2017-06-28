from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.core.validators import MaxValueValidator
import re
from datetime import datetime

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

def validateMonth (value):
	if value > 12:
		raise ValidationError("The maximum value is 12")
	return value

def validateYear (value):
	currentYear = datetime.now().year
	if value > currentYear:
		raise ValidationError("The maximum value is {}".format(currentYear))
	return value

def validateName (value):
	#if not re.match(r'^[\d\w\s\C\W]+$', value):
	if not re.match(r'[A-Z][a-z\-]+\s[A-Z][a-z\-]+$', value):	
		if not re.match(r'[A-Z][a-z\-]+\s[A-Z][a-z\.]+\s[A-Z][a-z\-]+$', value):
			raise ValidationError("Wrong form for this field")

	return value
	



		
