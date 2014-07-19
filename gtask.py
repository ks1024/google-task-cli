#! /usr/bin/env python

import gflags
import httplib2
import json
import argparse

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

service = None

def authenticate(json_data):
    FLAGS = gflags.FLAGS

    # Set up a Flow object to be used if we need to authenticate. This
    # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
    # the information it needs to authenticate. Note that it is called
    # the Web Server Flow, but it can also handle the flow for native
    # applications
    # The client_id and client_secret are copied from the API Access tab on
    # the Google APIs Console
    FLOW = OAuth2WebServerFlow(
        client_id=json_data['client_id'],
        client_secret=json_data['client_secret'],
        scope='https://www.googleapis.com/auth/tasks',
        user_agent='gTask/v1')

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
    global service
    service = build(serviceName='tasks', version='v1', http=http, developerKey=json_data['developerKey'])

def readCredentials():
    with open('credentials.json') as f:
        json_data = json.load(f)
        return json_data

def taskLists():
    tasklists = service.tasklists().list().execute()
    if len(tasklists) == 0:
        print "You don't have any task lists yet"
    else:
        i = 1
        for tasklist in tasklists['items']:
            print i, "-", tasklist['title']
            i+=1

def tasks(num):
    if num == 0:
        tasklist = service.tasklists().get(tasklist='@default').execute()
        print u'\u2588', tasklist['title']
        tasks = service.tasks().list(tasklist='@default').execute()
        i = 1
        for task in tasks['items']:
            print ' ', i, task['title']
            i+=1
    else:
        tasklists = service.tasklists().list().execute()
        if num > len(tasklists['items']):
            print "Please give a correct list number"
        else:
            tasklist = tasklists['items'][num-1]
            tasklistID = tasklist['id']
            print u'\u2588', tasklist['title']
            tasks = service.tasks().list(tasklist=tasklistID).execute()
            i = 1
            for task in tasks['items']:
                print ' ', i, task['title']
                i+=1


if __name__ == '__main__':
    json_data = readCredentials()
    authenticate(json_data)
    
    parser = argparse.ArgumentParser(description='A python CLI tool to manage your google tasks')
    parser.add_argument('-l', '--lists', action='store_true', help='show all your tasklists names')
    parser.add_argument('-t', '--tasks', action='store', metavar='listNumber', nargs='?', const='0', type=int,
                        help='show all tasks in the specified task list')
    
    args = parser.parse_args()

    if args.lists == True:
        taskLists()
    elif args.tasks != None:
        tasks(args.tasks)
