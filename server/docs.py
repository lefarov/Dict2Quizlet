
import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def main():
  SCOPES = ['https://www.googleapis.com/auth/documents']
  DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'
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


  service = build('docs', 'v1', credentials=creds)
  document = service.documents().get(documentId=DOCUMENT_ID).execute()

  print(f"The title of the document is: {document.get('title')}")


def create_doc():
  with open('server/token.pickle', 'rb') as token:
    creds = pickle.load(token)

  title = 'Test Document'
  body = dict(title=title)
  service = build('docs', 'v1', credentials=creds)

  doc = service.documents().create(body=body).execute()
  print(f"Created document with title: {doc.get('title')}")


if __name__ == "__main__":
  create_doc()
