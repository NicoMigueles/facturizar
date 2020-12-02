from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

TARGET_FOLDER = "FACTURAS ONLINE"


def descargarArchivo(item, service):
    if os.path.exists(f"facturas/{item['name']}"):
        #print(f"Skiping {item['name']} already exists.")
        return

    request = service.files().get_media(fileId=item['id'])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Downloaded {item['name']}.")

    with open(f"facturas/{item['name']}", "wb") as f:
        f.write(fh.getbuffer())


def updateFacturasFromDrive():
    """Descarga las ultimas facturas de drive
    """
    creds = None
    if os.path.exists('private/token.pickle'):
        with open('private/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'private/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('private/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    page_token = None
    results = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                   spaces='drive',
                                   fields='nextPageToken, files(id, name)',
                                   pageToken=page_token).execute()
    items = results.get('files', [])
    folder_id = None
    if not items:
        print('No files found.')
    else:

        for item in items:
            if item['name'] == TARGET_FOLDER:
                #print(f"Found {TARGET_FOLDER}, ID = {item['id']}")
                folder_id = item['id']
    results = service.files().list(q=f"'{folder_id}' in parents",
                                   fields='nextPageToken, files(id, name)',).execute()
    items = results.get('files', [])

    for item in items:
        descargarArchivo(item, service)
