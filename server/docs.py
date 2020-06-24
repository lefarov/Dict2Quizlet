
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


def get_folder_id(folder_name, creds):
  service = build('drive', 'v3', credentials=creds)
  folder_res = service.files().list(
    q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and not trashed", 
    fields='files(id)').execute()
  
  folder_ids = folder_res.get('files', [])
  if not folder_ids:
    raise ValueError(f"{folder_name} folder is not found in Google Drive")

  return folder_ids[0].get('id')


def list_docs(folder_id, creds):
  service = build('drive', 'v3', credentials=creds)
  files = service.files().list(
    q=f"mimeType = 'application/vnd.google-apps.document' and '{folder_id}' in parents and not trashed", 
    fields='files(id, name)').execute()

  return files.get('files', [])


def create_doc(name, folder_id, creds):
  service = build('drive', 'v3', credentials=creds)
  file_metadata = dict(name=name, 
                       parents=[folder_id],
                       mimeType='application/vnd.google-apps.document')
                       
  doc_file = service.files().create(body=file_metadata,
                                    fields='id').execute()

  return doc_file.get('id')


def append_transalation(translation, doc_id, creds):
  service = build('docs', 'v1', credentials=creds)
  document = service.documents().get(documentId=doc_id).execute()

  # TODO: there should be the easier way :(
  # Get the last content item to define the insertion index
  last_content_item = document.get('body').get('content')[-1]
  # Build the request
  requests = [
    { 'insertText': 
      { 'location': 
        { 'index': last_content_item.get('startIndex'), },
        'text': translation
      }
    },
  ]

  result = service.documents().batchUpdate(
    documentId=doc_id,
    body={'requests': requests}).execute()

  return result


if __name__ == '__main__':
  creds = get_creds()
  folder_id = get_folder_id('leo2quizlet', creds)

  print(list_docs(folder_id, creds))
  # doc_id = create_doc('Test from python 1', folder_id, creds)
  # for i in range(10):
  #   append_transalation(f"aaaa\t\t{i}\n", doc_id, creds)
