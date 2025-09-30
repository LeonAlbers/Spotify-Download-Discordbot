from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport import requests
import os , pickle
from dotenv import load_dotenv

load_dotenv()

PARENT_FOLDER_ID = os.getenv('PARENT_FOLDER_ID')

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_drive_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

creds = get_credentials()
drive_service = build('drive', 'v3', credentials=creds)

def create_folder(name):
    folder_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [PARENT_FOLDER_ID] if PARENT_FOLDER_ID else []
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    print(f'Folder "{name}" created with ID: {folder.get("id")}')
    return folder.get('id')

def list_folders():
    results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name, parents)').execute()
    items = results.get('files', [])
    if not items:
        print('No folders found.')
    else:
        print('Folders:')
        for item in items:
            print(f'{item["name"]} ({item["id"]})')
    return items

def delete_folder(folder_id):
    try:
        drive_service.files().delete(fileId=folder_id).execute()
        print(f'Folder with ID: {folder_id} deleted successfully.')
    except Exception as e:
        print(f'An error occurred: {e}')

def delete_all_folders():
    folders = list_folders()
    for folder in folders:
        if folder.get('parents') != None and folder['parents'][0] == PARENT_FOLDER_ID:
            delete_folder(folder['id'])
    print("All folders deleted.")

def upload_file(file_path, folder_id):
    print(f'Uploading file "{file_path}" to folder ID: {folder_id}')
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    print(f'File "{file_path}" uploaded to folder ID: {folder_id} with File ID: {file.get("id")}')
    os.remove(file_path)
    print(f'Local file "{file_path}" deleted after upload.')
    return file.get('id')

def make_folder_public(folder_id):
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    drive_service.permissions().create(fileId=folder_id, body=permission).execute()
    print(f'Folder with ID: {folder_id} is now public.')
    folder = drive_service.files().get(fileId=folder_id, fields='webViewLink').execute()
    print(f'Public link: {folder.get("webViewLink")}')
    return folder.get("webViewLink")