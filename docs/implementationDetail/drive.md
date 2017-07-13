# Introduction to Google Fusion Tables

This page will walk through the 'gdrive' app which is used to update the fusion table on google drive with google drive api. 

## Enable Google API

Before writing any code for the project, we need to enable two Google APIs. Since we need to use Google Drive and Google Fusion Table, so we need to enable both API.

1. Visit [Google Developer Console](https://console.developers.google.com/).

2. Look at the dashboard page if Google Fusion Table and Google Drive API has already be enabled. If not, then click on the library, and search for Google Fusion Table API and click on the button "ENABLE"

3. To enable the Google Drive API, we need to some more steps. All the steps to enable Google Drive API is in the page [Google Drive API Python](https://developers.google.com/drive/v3/web/quickstart/python). 

The only thing that you need to change is to change the name of the application to 'CAM2 Drive API'. 

After the final step to download client_secret.json file, you can continue to the next step.

## Install Google Client Library

Run the following command to install the library using pip:

```
pip install --upgrade google-api-python-client
```

## Authentication and upload files

After enable two APIs, you can start the project. I have already created the app 'gdrive' in this project. In the gdrive folder, you can see the python file called 'quickstart.py'. This is the file which uploads the file to the google drive.

```
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

```

The above code will take the information you have in the **client_secret.json** file get and create a file called **drive-python-quickstart.json** in the **~/.credentials/** directory. This file will be use to authenticate the use of google drive. 

```

file_metadata = { 'name' : 'cameraLocations',
                    'mimeType' : 'application/vnd.google-apps.fusiontable',
                    'parents': os.environ['PARENT_DIR_ID']
                    }
    media = MediaFileUpload('../../cameraLocations.csv',
                            mimetype='text/csv',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('Successful create File ID: %s' % file.get('id'))

```

The above code is used to upload the file into a particular directory. It only needs to execute once to create the file in the drive. After that, we only need to update the file in the directory. 

In the code,we need to add the id of the parent directory that we would like to place our file in. If you do not add the parent directory, then it will be place in the main directory. You can get the id of the google drive directory by clicking on the property of the directory.

After you execute this code, you can get the file id in the google drive. Write down the file id since you will need that in the next piece of code. 

```

file_metadata = { 'name' : 'cameraLocations',
                    'mimeType' : 'application/vnd.google-apps.fusiontable',
                    }
    media = MediaFileUpload('../../cameraLocations.csv',
                            mimetype='text/csv',
                            resumable=True)
    file = service.files().update(body=file_metadata,
                                        fileId=os.environ['SPREADSHEET_ID'],
                                        media_body=media,
                                        fields='id').execute()
    print ('Successful update File ID: %s' % file.get('id'))

```

After you upload the file, if the file on your local machine is changed, then the above code can be use to update the file on the driver. You need to use the fileID which you get in the previous upload section. You can also get the file id if you click on the property of the file on the google drive. After you add the fileID, you can update the file to the google drive. 

run the following code to create or update file.

```
python quickstart.py
```


## Create Fusion Table File

Since our file is ended with csv, so if we upload that CSV file to google drive, it will automatically converted into Google SpreadSheet. So we need to change that file into  Google Fusion Table

In google drive, click on new button, and choose "more" option to see if Google Fusion Table already exists in the google drive app. If not, then click on "Connect more apps". Find Google Fusion Table in the apps and add that into the google drive app. Then create new Google Fusion Table, and choose import it from spreadsheet. Then we can create our fusion table in google drive.


## Next Step

Now we have successfully create our fusion table in the google drive. However, it is not bonded with the spreadsheet in the drive so if spreadsheet is updated, it will not be updated. In the [Google Fusion Table](fusion_setup.md), we will write a function to trigger fusion table syncing as soon as google spreadsheet is uploaded. 

