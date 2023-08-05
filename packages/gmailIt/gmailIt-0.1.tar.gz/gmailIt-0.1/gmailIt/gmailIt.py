# useful ref:
# https://stackoverflow.com/a/43379469
# https://developers.google.com/gmail/api/guides/sending

# token.json: user auth file
# auth.json:  api auth file
import logging

from apiclient import errors, discovery
from googleapiclient.discovery import build

from httplib2 import Http
from oauth2client.file import Storage as userAuth
from oauth2client.tools import run_flow as getNewToken
from oauth2client.client import flow_from_clientsecrets as newToken


from base64 import urlsafe_b64encode as urlEncode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self, clientId, to, subject, plain, html):
        self.clientId = clientId
        self.to = to
        self.subject = subject
        self.plain = plain
        self.html = html

    def auth(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = 'https://www.googleapis.com/auth/gmail.send'
        tokenFile = userAuth('token.json')
        creds = tokenFile.get()

        # authenticate the user
        if not creds or creds.invalid:
            token = newToken('auth.json', SCOPES)
            creds = getNewToken(token, tokenFile)
        return build('gmail', 'v1', http=creds.authorize(Http()))

    def formatEmail(self):
        msg = MIMEMultipart('alternative')        
        msg['To'] = self.to
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.plain, 'plain'))
        msg.attach( MIMEText(self.html, 'html') )
        return {'raw': urlEncode(msg.as_bytes()).decode()}

    def send(self):
        try:
            email = self.formatEmail()
            return self.auth().users().messages().send(userId=self.clientId, body=email).execute()
        except errors.HttpError as error:
            logging.error(error)


