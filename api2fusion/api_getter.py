"""
Script to download all cameras from API. Check https://purduecam2project.github.io/CAM2WebUI/ for implementation details.
CAM2 WebUI team.
"""

import os
import time
import math

from apiclient import discovery
from apiclient.http import MediaFileUpload
from client import Client
from google.oauth2 import service_account
import pandas as pd

"""Global Variables"""

"""API"""
CLIENT_ID = str(os.environ['CLIENT_ID'])
CLIENT_SECRET = str(os.environ['CLIENT_SECRET'])
TOTAL_NO_CAMERAS = int(os.environ['TOTAL_NO_CAMERAS'])
FILE_ID = os.environ['FILE_ID']

"""Google Credentials"""
SCOPES = [
    'https://www.googleapis.com/auth/drive',
]
SERVICE_ACCOUNT_FILE = 'service.json'

"""Other"""
CSV_FILE = 'cam_data.csv'
SHEET_TITLE = 'web-API All Cameras'

"""
A dictionary the maps the header names to a name of parameter in the API. If None then it won't be updated on sheet.
It has to be the same order as the columns in the spreadsheet. The only exception is URL whose corresponding name would be
'url' as it's dependent on the camera type.

"""

SHEET_HEADERS = {
    'ID': 'cameraID',
    'Image': 'url',  # hardcoded in camera.py
    'Longitude': 'longitude',
    'Latitude': 'latitude',
    'City': 'city',
    'State': 'state',
    'Country': 'country',
    'Is Active Video': 'is_active_video',
    'Is Active Image': 'is_active_image',
    'Time Zone': None,
    'Time Zone ID': None,
    'Resolution Height': None,
    'Resolution Width': None,
    'Source': None,
    'Type': None,
    'Reference Logo': None,
    'Reference URl': None,
    'UTC offset': None,

}


def get_cams():
    """
    Calls the CAM2 API and returns the camera data as a
    list of dictionaries in Json format.
    Note: Current API is limited to 100 cameras per request.

    Returns list
    -------
        list of Camera objects
    """

    client = Client(clientID=CLIENT_ID, clientSecret=CLIENT_SECRET)
    offset = 0
    cams = []
    try:

        for x in range(0, int(math.ceil(TOTAL_NO_CAMERAS / 100))):  # No of reqests per 100 cameras
            print(".", end='', flush=True)
            cams.extend(client.search_camera(offset=offset))
            offset = offset + 100
        print('')
    except Exception as e:
        print("Exception while searching: " + str(e))
        raise (e)

    return (cams)


def write_csv(cams, filename):
    """
    Takes data from the new API and writes it to a CSV file for uploading

    Parameters
    ----------
    cams : list
        list of Camera Objects
    filename : str
        file name of the csv file
    """

    all_cams = []
    for cam in cams:
        all_cams.append([cam[v] for (k, v) in SHEET_HEADERS.items() if (v != None)])

    df = pd.DataFrame(all_cams, columns=[k for (k, v) in SHEET_HEADERS.items() if (v != None)])
    df.set_index('ID', inplace=True)
    print("Retrieved {0} cameras.".format(len(df.index)))
    df.to_csv(filename)


def upload_csv(csv_file, title, id):
    """
    Uploads the csv file to Google Drive.

    Parameters
    ----------
    csv_file : str
        csv file name
    title : str
        title of the spreadsheet to be created


    """



    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    driveService = discovery.build('drive', 'v3', credentials=credentials)
    file_metadata = {'name': title,
                     'mimeType': 'application/vnd.google-apps.fusiontable',
                     }
    media = MediaFileUpload(csv_file, mimetype='text/csv', resumable=True)

    try:
        file = driveService.files().update(body=file_metadata,
                                           fileId=id, media_body=media,
                                           fields='id').execute()

    except Exception as e:
        print('Exception while uploading: ' + str(e))
        raise (e)

    print('Successful update File ID: {0}'.format(file.get('id')))


def main():
    start_time = time.time()

    if(os.path.isfile(SERVICE_ACCOUNT_FILE) == False):
        raise Exception('Service file is missing or not named properly. Should be in same directory and called service.json')

    write_csv(get_cams(), CSV_FILE)
    upload_csv(CSV_FILE, title=SHEET_TITLE, id=FILE_ID)

    end_time = time.time()
    print("--- {0} seconds ---".format(end_time - start_time))


if __name__ == '__main__':
    main()
