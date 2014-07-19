#! /usr/bin/env python

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id='1045044932222-gkm68g0840p2kgp3cl6i4ek9ska766f7.apps.googleusercontent.com',
    client_secret='9tCjCFEz_ihrrqpRh1sRBW3N',
    scope='https://www.googleapis.com/auth/tasks',
    user_agent='pytask/v1')

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.

storage = Storage('tasks.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='tasks', version='v1', http=http, developerKey='AIzaSyBMA7l6Nwc_nkmmoX9W_ClUOER1MlS2Bs8')

def main():
    tasklists = service.tasklists().list().execute()

    for tasklist in tasklists['items']:
        print tasklist['title']

if __name__ == '__main__':
    main()
