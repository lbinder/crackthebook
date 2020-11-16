from __future__ import print_function
import pickle
import re
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def connect_to_gmail_api():
    """ Connect to GMAIL API """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def messages(service):
    """ Retrieve message in inbox """
    results = service.users().messages().list(userId='me', includeSpamTrash=False, q="from:me").execute()
    email_content = ""

    for mail in results['messages']:
        messages = service.users().messages().get(userId='me', id=mail["id"]).execute()
        email_content += str(base64.urlsafe_b64decode(messages['payload']['parts'][0]['body']['data']))

    return email_content


def valid(term):
    if term == '':
        return False

    if "\\r" in term:
        return False
    
    if "\\n" in term:
        return False

    return True


def parse_email(email_content):
    regex = r"\\r\\n\S*\\r\\n"
    matches = re.finditer(regex, email_content)
    words = {}
    for match in matches:
        term = match.group()[4:-4]
        if valid(term):
            #print(term)
            words[term] = ""
    print(count)
    return words


def vocab():
    service = connect_to_gmail_api()
    email_content = messages(service)
    words = parse_email(email_content)
    