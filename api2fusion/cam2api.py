import requests
import json
import os


class APIClient(object):
    """

    """

    MAIN_URL = 'https://cam2-api.herokuapp.com'
    TEST_URL = 'https://cam2-api-test.herokuapp.com'
    # CLIENT_ID = os.environ['CAM2_CLIENT_ID']
    # CLIENT_SECRET = os.environ['CAM2_CLIENT_SECRET']
    CLIENT_ID = 'webUI'
    CLIENT_SECRET = 'webUI'

    def __init__(self):
        """

        Parameters
        ----------
        _url :
        token :
        """

        self._url = APIClient.MAIN_URL
        self._token = None  # Equals 0 if the request is for a Token

    @property
    def url(self):
        """

        Returns
        -------

        """
        return self._url

    @url.setter
    def url(self, url):
        """

        Parameters
        ----------
        url :

        Returns
        -------

        """
        self._url = url

    @property
    def token(self):
        """

        Returns
        -------

        """
        return self._token

    @token.setter
    def token(self, token):
        """

        Parameters
        ----------
        toke :

        Returns
        -------

        """
        self._token = token

    def __execute(self, resource, method, querystring=None):
        """

        Parameters
        ----------
        querystring :

        Returns
        -------

        """


        header = None
        if self._token != None:
            header = self.header_builder()


        print(header)
        response = requests.request(method=method, url=self._url + resource, headers=header, params=querystring)

        # print(response)
        data = response.json()
        return data

    def authorize(self):
        """

        Returns
        -------

        """

        querystring = {'clientID': APIClient.CLIENT_ID, 'clientSecret': APIClient.CLIENT_SECRET}
        resource = '/auth'
        response = self.__execute(method='GET', resource=resource, querystring=querystring)
        self._token = response["token"]
        print(self._token)
        return self

    def search(self, latitude=None, longitude=None, radius=None, type=None, source=None,
               country=None, state=None, city=None, resolution_width=None, resolution_height=None,
               is_active_image=None, is_active_video=None, offset=None):
        """

        Parameters
        ----------
        latitude :
        longitude :
        radius :
        type :
        source :
        country :
        state :
        city :
        resolution_width :
        resolutione_height :
        is_active_image :
        is_active_vide :
        offset :

        Returns
        -------

        """

        querystring = {
            'latitude': latitude,
            'longitude': longitude,
            'radius': radius,
            'type': type,
            'source': source,
            'country': country,
            'state': state, 'city': city,
            'resolution_width': resolution_width,
            'resolution_height': resolution_height,
            'is_active_image': is_active_image,
            'is_active_video': is_active_video,
            'offset': offset
        }

        resource = '/cameras/search'
        response = self.__execute(method='GET', resource=resource, params=querystring)
        return response

    def get_by_id(self, id):
        """

        Parameters
        ----------
        id :

        Returns
        -------

        """
        if id == None:
            raise ValueError("ID argument required")

        resource = '/cameras/' + str(id)
        camera = self.__execute(method='GET', resource=resource)
        return camera

    def header_builder(self):
        """

        Returns
        -------

        """
        head = {'Authorization': 'Bearer ' + str(self.token)}
        return head
