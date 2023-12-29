import os
import base64
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Constants
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Set up Gmail API connection
def create_gmail_service():
    credentials = None

    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json')
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    service = build(API_NAME, API_VERSION, credentials=credentials)
    return service

# Fetch emails using Gmail API
def get_emails(service):
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    return messages

# Streamlit app layout
def app_layout():
    st.sidebar.title('Email App')

    # OAuth and API setup
    st.warning("Please run this app with '--server.enableCORS=False' to enable OAuth in the Streamlit app.")
    service = create_gmail_service()

    st.title('Inbox - Gmail')  # Change this to the appropriate email provider
    search_input = st.text_input('Search', '')

    # Display emails or show a message if no emails
    if st.button('Load Emails'):
        emails = get_emails(service)

        if emails:
            for email in emails:
                message = service.users().messages().get(userId='me', id=email['id']).execute()
                subject = next(h['value'] for h in message['payload']['headers'] if h['name'] == 'Subject')
                sender = next(h['value'] for h in message['payload']['headers'] if h['name'] == 'From')
                date = next(h['value'] for h in message['payload']['headers'] if h['name'] == 'Date')
                body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')

                st.write(f"From: {sender}")
                st.write(f"Subject: {subject}")
                st.write(f"Date: {date}")
                st.write(f"Content: {body}")
                st.write('---')
        else:
            st.write('No emails found.')

# Streamlit app
if __name__ == '__main__':
    app_layout()
