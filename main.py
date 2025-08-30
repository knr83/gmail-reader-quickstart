"""
Simple Gmail Reader - Quick access to Gmail

What it does:
- Connects to your Gmail
- Shows last 5 emails
- Displays subject, sender and date

Setup (one time only):
1. Download credentials.json from Google Cloud Console
2. Put it in this folder
3. Run script - browser will open for authorization

"""

import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Read-only access to Gmail (safe!)
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    """Gets access to Gmail"""
    
    # Check if there's already a saved token
    if os.path.exists("token.json"):
        print("Found saved authorization token...")
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        creds = None
    
    # If no token or expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(Request())
        else:
            # First authorization needed
            if not os.path.exists("credentials.json"):
                print("ERROR: credentials.json file not found!")
                print("Download it from Google Cloud Console and put it in this folder")
                return None
            
            print("First authorization...")
            print("Browser will open - allow access to Gmail")
            
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for next runs
        with open("token.json", "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print("Token saved!")
    
    # Create Gmail service
    return build("gmail", "v1", credentials=creds)

def get_emails_data(service, count=5):
    """Gets emails data and returns as list"""
    
    # Get list of message IDs
    result = service.users().messages().list(userId="me", maxResults=count).execute()
    messages = result.get("messages", [])
    
    if not messages:
        return []
    
    emails_data = []
    
    for message in messages:
        msg = service.users().messages().get(
            userId="me", 
            id=message["id"], 
            format="metadata",
            metadataHeaders=["Subject", "From", "Date"]
        ).execute()
        
        headers = msg.get("payload", {}).get("headers", [])
        subject = "No subject"
        sender = "Unknown"
        date = "No date"
        
        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"] or "No subject"
            elif header["name"] == "From":
                sender = header["value"] or "Unknown"
            elif header["name"] == "Date":
                date = header["value"] or "No date"
        
        email_data = {
            "id": message["id"],
            "threadId": msg.get("threadId"),
            "subject": subject,
            "sender": sender,
            "date": date,
            "snippet": msg.get("snippet", "")
        }
        
        emails_data.append(email_data)
    
    return emails_data

def main():
    """Main function"""
    
    print("Starting Gmail Reader...")
    print("=" * 50)
    
    service = get_gmail_service()
    if not service:
        print("\nFailed to connect to Gmail")
        print("Check credentials.json file")
        return
    
    print("Successfully connected to Gmail!")
    
    emails_data = get_emails_data(service, count=5)
    
    if emails_data:
        # Save to JSON file
        with open("emails.json", "w", encoding="utf-8") as f:
            json.dump(emails_data, f, ensure_ascii=False, indent=2)
        
        print(json.dumps(emails_data, ensure_ascii=False, indent=2))
        
        print(f"\nSaved {len(emails_data)} emails to emails.json")
    else:
        print("No emails found")

if __name__ == "__main__":
    main()
