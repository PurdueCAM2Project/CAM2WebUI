# Python script to create JSON file of country codes mapped to country viewports
# See this link for extensive documentation: https://purduecam2project.github.io/CAM2WebUI/implementationDetail/load_latlngJSON.html#
# Author: Deeptanshu Malik

from django.core.management.base import BaseCommand, CommandError
import urllib.request, urllib.parse, urllib.error
import requests
import ssl
from bs4 import BeautifulSoup
import json
from time import sleep

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
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


    def handle(self, *args, **options):
        countries = self.get_countries_from_webpage()
        countries = self.geocode_data(countries)

        with open('app/static/app/js/countries_viewport.json', "w") as writeJSON:
            json.dump(countries, writeJSON, indent=2)
