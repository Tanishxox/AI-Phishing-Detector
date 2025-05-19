import os
import pickle
import base64
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate Gmail API and return service object"""
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

def clean_email_text(text):
    """Clean email text by removing HTML tags, images, and unnecessary patterns"""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\[image:[^\]]+\]', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def fetch_latest_emails(service, max_results=5):
    """Fetch the latest emails from the user's Gmail inbox"""
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"], format='full').execute()
        payload = msg_data["payload"]
        headers = payload.get("headers", [])

        email_data = {"subject": "No Subject", "body": "No Body"}

        for header in headers:
            if header["name"] == "Subject":
                email_data["subject"] = header["value"]
                break

        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    if "body" in part and "data" in part["body"]:
                        body_data = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        email_data["body"] = clean_email_text(body_data)
                        break
        elif "body" in payload and "data" in payload["body"]:
            body_data = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
            email_data["body"] = clean_email_text(body_data)

        emails.append(email_data)

    return emails