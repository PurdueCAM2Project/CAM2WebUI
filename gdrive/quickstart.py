from __future__ import print_function
import httplib2
import os

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

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = '../../client_secret.json'
APPLICATION_NAME = 'CAM2 Drive API'


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

def getfiles(service):
    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    """
    items = getfiles(service)
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
    """

    """
    file_metadata = { 'name' : 'cameraLocations',
                    'mimeType' : 'application/vnd.google-apps.fusiontable',
                    'parents': os.environ['PARENT_DIR_ID']
                    }
    media = MediaFileUpload('files/cameraLocations.csv',
                            mimetype='text/csv',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('Successful create File ID: %s' % file.get('id'))
    
    """
    file_metadata = { 'name' : 'cameraLocations',
                    'mimeType' : 'application/vnd.google-apps.fusiontable',
                    }
    media = MediaFileUpload('files/cameraLocations.csv',
                            mimetype='text/csv',
                            resumable=True)
    file = service.files().update(body=file_metadata,
                                        fileId=os.environ['SPREADSHEET_ID'],
                                        media_body=media,
                                        fields='id').execute()
    print ('Successful update File ID: %s' % file.get('id'))
    

if __name__ == '__main__':
    main()