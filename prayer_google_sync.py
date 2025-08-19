#!/usr/bin/env python3

from datetime import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from icalendar import Calendar

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def parse_ics_events(file_path="prayer_times.ics"):
    with open(file_path, 'rb') as f:
        cal = Calendar.from_ical(f.read())
    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = str(component.get('summary'))
            location = str(component.get('location', ''))
            dtstart = component.decoded('dtstart')
            dtend = component.decoded('dtend')
            if isinstance(dtstart, datetime) and isinstance(dtend, datetime):
                events.append((summary, dtstart, dtend, location))
    return events

def create_event(service, summary, start_dt, end_dt, location):
    event = {
        'summary': summary,
        'location': location,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'Europe/Berlin',
        },
        'reminders': {'useDefault': True},
    }
    # 👇 NEW: choose target calendar ## For multiple possible calendars: (env var or default to 'primary')
    # calendar_id = os.getenv('CALENDAR_ID', 'primary')
    calendar_id = '41929802da9a7eb1dc226bd6356f6afd325aa0c67d2e9951c32a5f0829359564@group.calendar.google.com'

    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"✅ Created: {created['summary']} on {created['start']['dateTime']}")

if __name__ == "__main__":
    service = authenticate_google()

    events = parse_ics_events("prayer_times.ics")
    for summary, start, end, location in events:
        create_event(service, summary, start, end, location)

