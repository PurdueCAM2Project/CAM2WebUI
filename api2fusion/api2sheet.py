import pygsheets
import json
from cam2api import *

SPREADSHEET_NAME = 'habal'
MAIN_URL = 'https://cam2-api.herokuapp.com'
TEST_URL = 'https://cam2-api-test.herokuapp.com'
GOOGLE_SPREADSHEET_SERVICE = 'sheets'
GOOGLE_SPREADSHEET_SERVICE_VERSION = 'v4'
SERVICE_ACCOUNT_FILE = "service.json"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]







if __name__ == "__main__":

    try:
        gc = pygsheets.authorize(service_file=SERVICE_ACCOUNT_FILE)
        gs = gc.open("habal")
        gs.share("nourehab97@gmail.com", role='writer')
        wks = gs.sheet1

        #TODO figure out why the API is not authorizing the call

        # unauth_req = APIClient()
        # unauth_req.url = APIClient.TEST_URL
        # print(unauth_req.url)
        # api = unauth_req.authorize()
        # camera = api.get_by_id('5b50e773b5fbfa0004434ad2')
        # print(camera)


        #TODO get the camera

        #TODO get the camera fields

        #TODO check if camera exists in the sheet

        #TODO if yes -> update that row

        #TODO if no -> append a new row



        id_list = wks.get_col(col=1)  # last parameter doesn't work
        if(id in id_list):
            update

        print(id_list.index('5b16ebc75487e70004aa476b'))

    except Exception as e:
        print(e)
