import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class GoogleCalendar:
  
  """
    Google contructor provider methods for manager calendar
      Args:
      * tokenFile (str): The path to the authorized user json file.
      * credentialsFile (str): The path to the authorized crdentials json file.

      Returns Methods:
      * list_events: function returns summary ans description
  """
  def __init__(self, tokenFile: str, credentialsFile: str) -> None:
      self.tokenFile = tokenFile
      self.credentialsFile = credentialsFile
      self.service = self._authenticate()

  def _authenticate(self):
    try:
      creds = None

      if os.path.exists(self.tokenFile):
        creds = Credentials.from_authorized_user_file(self.tokenFile, SCOPES)
        
      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
          
        else:
          flow = InstalledAppFlow.from_client_secrets_file(self.credentialsFile, SCOPES)
          creds = flow.run_local_server()
          
        with open(self.tokenFile, "w") as token:
          token.write(creds.to_json())
      return build("calendar", "v3", credentials=creds)
    
    except BaseException  as a:
      print(f"Error: {a}")
      
  def list_events(self):
    
    now = datetime.datetime.utcnow().isoformat() + "Z"
    
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59).isoformat() + "z"
    
    data_events = self.service.events().list(
      calendarId="primary",
      timeMin=now,
      timeMax=tomorrow,
      singleEvents=True,
      orderBy="startTime"
    ).execute()
    
    events = data_events.get('items', [])
    
    if not events:
        print("No upcoming events found.")
        return

    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      
      if not event.get("description", None):
        print('não avaliado')
      else:
        print(start, event["summary"])      
        print(start, event["description"])
    
if __name__ == "__main__":
  calendar = GoogleCalendar(tokenFile="token.json", credentialsFile="credentials.json")
  calendar.list_events()