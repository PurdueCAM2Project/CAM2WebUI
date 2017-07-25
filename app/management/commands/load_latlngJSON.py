from django.core.management.base import BaseCommand, CommandError
import urllib.request, urllib.parse, urllib.error
import ssl
from bs4 import BeautifulSoup


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
        country_menu = soup.find('select', id="country")
        print(country_menu.prettify())


    def handle(self, *args, **options):
        self.stdout.write("testing")