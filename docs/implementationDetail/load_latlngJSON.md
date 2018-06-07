# load_latlngJSON

## What is it
It is a custom Django command to execute the load_latlngJSON.py script. 

Main purpose of this script is to create a dictionary in the form a JSON object to proivde O(1) lookup for latitudinal and longitudinal information of  northeast and southwest corners of a country. This information is needed to dynamically adjust viewport of map as multiple countries are selected.

This command is used to execute a scripts that parses all countries listed on our project's cameras webpage, uses geocode API to obtain viewport of each country, and then creates a JSON file of country codes mapped to country viewports.

## Why it was needed
See [this issue](https://github.com/PurdueCAM2Project/CAM2WebUI/issues/95) for an in-depth explanation.

A brief summary: this script is a necessary solution to 
1. Limit calls to geocode API: there's a limit to number of free requests to geocode API which would have been undoubtedly exceeded in times of relatively heavy traffic to our website.
2. Increase speed performace of our website's cameras page: geocoder API requests may take several hundered milliseconds and this results in a subpar user experience when multiple countries are selected, in fact, dynaymically adjusting viewport when more than 3 countries are selected becomes infeasbile

## Executing the script

```
python manage.py load_latlngJSON
```

This will print relevant message to to the console for each country as it is successfully, or not, geocoded. If this is not desired then the output can be piped to a dummy file where it can be examined. 

```
python manage.py load_latlngJSON > dummy.txt
```

The script can run for potentially more than 2 minutes, due to reasons explained [here](#delay_reason) and [here](https://github.com/PurdueCAM2Project/CAM2WebUI/commit/b725343182ae964cbd2a3a44cb72d379a11b4c2e).

## Documentation

The script was setup as per the [official tutorial](https://docs.djangoproject.com/en/dev/howto/custom-management-commands/) on how to create a custom Django command.

The path to the script: /app/management/commands/load_latlngJSON.py

<div class="admonition note">
<p class="first admonition-title">Note</p>
<p class="last"Tthe path to the script, the 'Command' class definition and the 'handle' member function definition must not be modified as they are necessary for the custom command to be recognized by Django.
.</p>
</div>

Each time the script is executed, the handle member funtion of the Command class is called

```
    def handle(self, *args, **options):
        countries = self.get_countries_from_webpage()
        countries = self.geocode_data(countries)

        with open('app/static/app/js/countries_viewport.json', "w") as writeJSON:
            json.dump(countries, writeJSON)
```
#### Using Beautiful Soup to parse webpage

As explained in the [CAM2 Training docs](https://github.com/PurdueCAM2Project/Training#introduction-to-beautiful-soup-and-selenium), Beautiful Soup was used to parse the list of countries for our website's cameras page.

[This](http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html) webpage from stanford.edu is also an excellent quick guide to Beautiful Soup
```
import urllib.request, urllib.parse, urllib.error
import ssl
from bs4 import BeautifulSoup
```
```
    def get_countries_from_webpage(self):
        #ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        #get country select tag
        url = "http://www.cam2project.net/cameras/"
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        country_menu = soup.find('select', id="country").find_all('option')

        countries = {}
        for country in country_menu:
            if country['value']:
                countries[country['value']] =  str(country.text)

        return countries
```

#### Using geocode API
Google's geocode API was used to obtain viewports of countries listed on our website's drop down menu. 

These viewports are nested dictionaries containing information about the latitudinal and longitudinal positions of the northwest and southwest corners of a country.

[This](https://gist.github.com/pnavarrc/5379521) tutorial on Github was referred to as a guide to use geocode API in python.

The geocoding function takes a dictionary of country codes mapped to country names as inputs and makes requests using country names to obtain viewports. Each country's code is then mapped to country's viewport. The resulting dictionary is then returned.

- It is necessary for the script to sleep for 0.01 secounds before making a request to geocode API in order to ensure that the 50 queries per second limit is not exceeded.
- <a name="delay_reason">Initially not all countries were geocoded properly, each time geocoding randomly failed for a number of consecutively listed countries. This was solved by waiting for 1 second in the event of failure and then sending the same request to geocode API again. Now 100% of the countries are geocoded each time the script is executed. However, as a consequence, the script may take more than 2 minutes to run.</a>

```
import requests
from time import sleep
```
```
    def geocode_data(self, countries):
        GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

        for country_code, country_name in countries.items():
            #to enfore geocode 50 queries per second limit
            sleep(0.01)

            #make the request and get the response data
            req = requests.get(GOOGLE_MAPS_API_URL, params= {
                'address': country_name
            })
            res = req.json()

            if(res['status'] != 'OK'):
                print(country_code, country_name)
                continue
            else:
                sleep(1)
                req = requests.get(GOOGLE_MAPS_API_URL, params={
                    'address': country_name
                })
                res = req.json()
                if (res['status'] != 'OK'):
                    print("Failed 2nd attempt: ", country_code, country_name)
                    continue
                print("OK: ", country_code, country_name)

            #Use the first result
            result = res['results'][0]

            countries[country_code] = result['geometry']['viewport']

        return countries
```

#### Creating JSON file

Once the nested dictionary of country codes mapped to country viewports is obtained, 'json' library is used to create a JSON file of this dictionary in the appropriate directory:

```
import json
```
```
with open('app/static/app/js/countries_viewport.json', "w") as writeJSON:
    json.dump(countries, writeJSON)
```
