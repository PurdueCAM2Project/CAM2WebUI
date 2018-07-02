import json
import httplib2
import os
import requests
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

"""Global Variables"""

"""API"""
CLIENT_ID = os.environ['CAM2_CLIENT_ID']
CLIENT_SECRET = os.environ['CAM2_CLIENT_SECRET']
MAIN_URL = 'https://cam2-api.herokuapp.com'
TOTAL_NO_CAMERAS = 1290  # No of reqests per 100 cameras

"""Google Credentials"""
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'New Camera Map'
FILE_ID = os.environ['SPREADSHEET_FILE_ID']

"""Other"""
CSV_FILE = 'cam_data.csv'


class ApiRequest(object):
    def __init__(self, url, token):
        self.url = url
        self.auth = token  # Equals 0 if the request is for a Token

    def get_Api_Request(self, querystring):
        header = {
            'Authorization': "Bearer " + self.auth,
            }
        response = requests.get(self.url, headers=header, params=querystring)
        data = response.json()
        return data

    def get_Token(self):
        querystring = {'clientID': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
        response = requests.request("GET", self.url, params=querystring)
        token = (json.loads(str(response.text)))['token']
        return token
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_api_data():


    """Calls the CAM2 API and returns the camera data as a
    list of dictionaries in Json format.
    Note: Current API is limited to 100 cameras per request. """


    # Gets Token
    token_request = ApiRequest(MAIN_URL + "/auth",0)
    token = token_request.get_Token()

    # Gets Data
    camera_data = list()
    data_request = ApiRequest(MAIN_URL + '/cameras/search', token)
    offset = 0
    for x in range(0,1290):
        querystring = {'offset': offset}
        data = data_request.get_Api_Request(querystring)
        offset = offset + 100
        camera_data.append(data)
        """ Only use when Script is Failing
        time.sleep(60)
        """

    return(camera_data)

def get_credentials():


    """Gets credentials in order to use google API"""


    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                'drive-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials

def write_csv():


    """Takes data from the new API and writes it to a CSV file for uploading"""


    data = get_api_data()
    with open(CSV_FILE, 'w') as camData:
        camData.write('ID, Image, Latitude, Longitude, City, State, Country')
        camData.write('\n')
        for hundred in data:
            for camera in hundred:
                try:
                    id = camera['cameraID']
                    if id is None:
                        id = ''
                    path = ''
                    if camera['type'] == 'ip':
                        ip_address = camera['retrieval']['ip']
                        if ip_address is None:
                            ip_address = ''
                        video_path = camera['retrieval']['video_path']
                        if video_path is None:
                            video_path = ''
                        path = 'http://' + ip_address + video_path
                    elif camera['type'] == 'non_ip':
                        path = camera['snapshot_url']
                    elif camera['type'] == 'stream':
                        path = camera['m3u8_url']
                    latitude = str(camera['latitude'])
                    longitude = str(camera['longitude'])
                    city = camera['city']
                    if city is None:
                        city = ''
                    state = camera['state']
                    if state is None:
                        state = ''
                    country = camera['country']
                    if country is None:
                        country = ''

                    camData.write('' + id + ', ' + path + ', ' + latitude + ', '
                    + longitude + ', ' + city + ', ' + state + ', '
                    + country + '\n')
                except:
                    continue

def upload_csv():


    """Uplodes the Csv to Google Drive """


    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    file_metadata = { 'name' : 'All Cameras',
                    'mimeType' : 'application/vnd.google-apps.fusiontable',
                    }
    media = MediaFileUpload('cam_data.csv',mimetype='text/csv',resumable=True)
    file = service.files().update(body=file_metadata,
                                    fileId=FILE_ID,media_body=media,
                                    fields='id').execute()
    print ('Successful update File ID: %s' % file.get('id'))

def main():
    start_time = time.time()
    write_csv()
    upload_csv()
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
