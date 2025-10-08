from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport import requests
import os , pickle
from tools.consoleStyling import fonts
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
    print(f'{fonts.CYAN + fonts.BOLD}Folder "{name}" created with ID:{fonts.END} {folder.get("id")}')
    return folder.get('id')

def list_folders():
    results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name, parents)').execute()
    items = results.get('files', [])
    if not items:
        print(f'{fonts.RED + fonts.BOLD}No folders found.{fonts.END}')
    else:
        print(f'{fonts.CYAN + fonts.BOLD}Folders:{fonts.END}')
        for item in items:
            print(f'{item["name"]} ({item["id"]})')
    return items

def delete_folder(folder_id):
    try:
        drive_service.files().delete(fileId=folder_id).execute()
        print(f'{fonts.CYAN + fonts.BOLD}Folder with ID: {folder_id} deleted successfully.{fonts.END}')
    except Exception as e:
        print(f'{fonts.RED + fonts.BOLD}An error occurred:{fonts.END} {e}')

def delete_all_folders():
    folders = list_folders()
    for folder in folders:
        if folder.get('parents') != None and folder['parents'][0] == PARENT_FOLDER_ID:
            delete_folder(folder['id'])
    print(f"{fonts.CYAN + fonts.BOLD}All folders deleted.{fonts.END}")

def upload_file(file_path, folder_id):
    print(f'{fonts.CYAN + fonts.BOLD}Uploading file{fonts.END} "{file_path}" to folder ID: {folder_id}')
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    os.remove(file_path)
    print(f'{fonts.CYAN + fonts.BOLD}Uploaded file{fonts.END} "{file_path}" {fonts.CYAN + fonts.BOLD}to folder ID:{fonts.END} {folder_id} {fonts.CYAN + fonts.BOLD}with File ID:{fonts.END} {file.get("id")}')
    print(f'{fonts.CYAN + fonts.BOLD}Local file {fonts.END}"{file_path}" {fonts.CYAN + fonts.BOLD}deleted after upload.{fonts.END}')
    return file.get('id')

def make_folder_public(folder_id):
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    drive_service.permissions().create(fileId=folder_id, body=permission).execute()
    print(f'{fonts.CYAN + fonts.BOLD}Folder with ID: {folder_id} is now public.{fonts.END}')
    folder = drive_service.files().get(fileId=folder_id, fields='webViewLink').execute()
    print(f'{fonts.CYAN + fonts.BOLD}Public link:{fonts.END} {folder.get("webViewLink")}')
    return folder.get("webViewLink")