
import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_creds():
  SCOPES = [
    'https://www.googleapis.com/auth/documents', 
    'https://www.googleapis.com/auth/drive'
  ]
  creds = None

  if os.path.exists('server/token.pickle'):
    with open('server/token.pickle', 'rb') as token:
        creds = pickle.load(token)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('server/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('server/token.pickle', 'wb') as token:
        pickle.dump(creds, token)

  return creds


def create_doc(creds):
  title = 'Test Document'
  body = dict(title=title)
  service = build('docs', 'v1', credentials=creds)

  doc = service.documents().create(body=body).execute()
  print(f"Created document with title: {doc.get('title')}")


def list_files(folder_name, creds):
  service = build('drive', 'v3', credentials=creds)
  folder_res = service.files().list(
    q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'", 
    fields="files(id)").execute()
  
  folder_ids = folder_res.get('files', [])
  if folder_ids:
    folder_id = folder_ids[0].get('id')
  else:
    raise ValueError("leo2dict folder is not found in Google Drive")

  files = service.files().list(
    q=f"mimeType = 'application/vnd.google-apps.document' and '{folder_id}' in parents", 
    fields="files(id, name)").execute()

  return files.get('files', [])

if __name__ == "__main__":
  creds = get_creds()
  print(list_files("leo2quizlet", creds))
