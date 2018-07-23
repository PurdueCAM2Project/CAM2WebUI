from apiclient import discovery
from google.oauth2 import service_account
import os

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
]
SERVICE_ACCOUNT_FILE = 'service.json'
SHEET_TITLE = 'cam2'






def main():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    sheetService = discovery.build('sheets', 'v4', credentials=credentials)

    spreadsheet = {
        'properties': {
            'title': SHEET_TITLE
        }
    }

    cam2sheet = sheetService.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    spreadsheetId = cam2sheet.get('spreadsheetId')

    print('Successful update File ID: {0}'.format(spreadsheetId))


if __name__ == '__main__':
   main()
