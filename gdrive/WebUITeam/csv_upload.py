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

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'New Camera Map'
FILE_ID = '15E5F5nA00C8zfaBxo42d4jOtNQ3F7zPDlNbGeKwrlwA'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
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
    """Takes data from the new API and writes it to a CSV file for uploading 
    
    Initial Testing uses data from a prepared json file with 1000 cameras. Final script will load directly from the API
    
    """
    data = get_api_data()
    """with open('cam_data.json') as f:
        data = json.load(f)"""
    with open('cam_data.csv', 'w') as camData:
        camData.write('ID, Image, Latitude, Longitude, City, State, Country')
        camData.write('\n')
        for d in data:
            cid = d['cameraID']
            if cid is None:
                cid = ''
            cpath = ''
            if d['type'] == 'ip':
                cip = d['retrieval']['ip']
                if cip is None:
                    cip = ''
                cvp = d['retrieval']['video_path']
                if cvp is None:
                    cvp = ''
                cpath = 'http://' + cip + cvp
            elif d['type'] == 'non_ip':
                cpath = d['snapshot_url']
            elif d['type'] == 'stream':
                cpath = d['m3u8_url']
            lat = str(d['latitude'])
            lng = str(d['longitude'])
            ccity = d['city']
            if ccity is None:
                ccity = ''
            cstate = d['state']
            if cstate is None:
                cstate = ''
            ccountry = d['country']
            if ccountry is None:
                ccountry = ''
            camData.write('' + cid + ', ' + cpath + ', ' + lat + ', ' + lng + ', ' + ccity + ', ' + cstate + ', ' + ccountry)
            camData.write('\n')

def upload_csv():
    """Uses the credentials specific to the Team/Project to upload a CSV to a specified Google Spreadsheet

    Note that in production the fileId specified below should be an environment variable, for security purposes. 
    
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    file_metadata = { 'name' : 'All Cameras',
                    'mimeType' : 'application/vnd.google-apps.fusiontable',
                    }
    media = MediaFileUpload('cam_data.csv',
                            mimetype='text/csv',
                            resumable=True)
    file = service.files().update(body=file_metadata,
                                        fileId=FILE_ID,
                                        media_body=media,
                                        fields='id').execute()
    print ('Successful update File ID: %s' % file.get('id'))

def get_api_data():
    """Old function used to pull data from the API and write it to a JSON file.

    Very much requires re-writing and clean-up to use with this new code, but it's useful as a starting point. 

    """
    client = '34b9eb8afc032098bc96174ec38ca2dba940a401d03c311251af4d8b609f7272c91ed0aaef1ee4eddb4783bcaa3ead7d'
    secret = 'b0eaea176c29331149557b1c2fe54b82d335c8c30dbed9a50c5e4aa141b15dbefbbfd69'
    params = {'clientID': client, 'clientSecret': secret}
    rauth = requests.get('https://cam2-api.herokuapp.com/auth', params=params)
    token = rauth.json()['token']
    headerval = 'Bearer ' + token
    header = {'Authorization': headerval}
    r = requests.get('https://cam2-api.herokuapp.com/cameras/search', headers=header)
    data = r.json()
    output = list()
    for d in data:
        output.append(d)
    count = 0
    #while True:
    for x in range(1,10):
        time.sleep(60)
        count = count + 100
        rauth = requests.get('https://cam2-api.herokuapp.com/auth', params=params)
        token = rauth.json()['token']
        headerval = 'Bearer ' + token
        header = {'Authorization': headerval}
        param2 = {'offset': count}
        tr2 = requests.get('https://cam2-api.herokuapp.com/cameras/search', params=param2, headers=header)
        print(tr2.status_code)
        if tr2.status_code != 200:
            continue
        tdata2 = tr2.json()
        for d2 in tdata2:
            output.append(d2)
        if len(tr2.json()) < 100:
            break
    return output

def main():
    write_csv()
    upload_csv()

if __name__ == '__main__': 
    main()
