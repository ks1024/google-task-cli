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

def getTaskLists():
    tasklists = service.tasklists().list().execute()
    if len(tasklists) == 0:
        print "You don't have any task lists yet"
    else:
        for i, tasklist in enumerate(tasklists['items']):
            print i+1, "-", tasklist['title']

def getTasks(opts):
    list_num = opts[0]
    tasklists = service.tasklists().list().execute()
    if list_num > len(tasklists['items']) or list_num == 0:
        print "[ERROR] Please give a correct list number"
    else:
        tasklist = tasklists['items'][list_num-1]  # get the specified task list object
        tasklistID = tasklist['id']  # get the specified task list ID
        tasks = service.tasks().list(tasklist=tasklistID).execute()
        if 'items' in tasks:
            print u'\u2588', tasklist['title'] # print task list title
            for i, task in enumerate(tasks['items']):
                print ' ', i+1, task['title']
        else:
            print "[WARNNING] The task list '" + tasklist['title'] + "' has not yet any tasks"

def createNewTaskList(list_title):
    new_tasklist = {
        'title': list_title
    }
    result = service.tasklists().insert(body=new_tasklist).execute()
    print "[SUCCESS] The new task list '" + result['title'] + "' has been created"

def updateTaskList(opts):
    list_num, list_title = opts
    list_num = int(list_num)
    tasklists = service.tasklists().list().execute()
    if list_num > len(tasklists['items']) or list_num == 0:
        print "[ERROR] Please give a correct list number"
    else:
        tasklist = tasklists['items'][list_num-1]
        tasklistID = tasklist['id']
        list_old_title = tasklist['title']
        tasklist['title'] = list_title
        result = service.tasklists().update(tasklist=tasklistID, body=tasklist).execute()
        print "[SUCCESS] Update the task list '" + list_old_title + "' to '" + result['title'] + "'"

def delTaskList(opts):
    list_num = opts[0]
    tasklists = service.tasklists().list().execute()
    if list_num > len(tasklists['items']) or list_num == 0:
        print "[ERROR] Please give a correct list number"
    else:
        tasklist = tasklists['items'][list_num-1]
        tasklistID = tasklist['id']
        list_old_title = tasklist['title']
        service.tasklists().delete(tasklist=tasklistID).execute()
        print "[SUCCESS] The tast list '" + list_old_title + "' has been deleted"

def createNewTask(opts):
    list_num = opts[0]
    tasklists = service.tasklists().list().execute()
    if list_num > len(tasklists['items']) or list_num == 0:
        print "[ERROR] Please give a correct list number"
        return
    title = raw_input("Task title: ")
    notes = raw_input("Task notes: ")
    due = raw_input("Task due (YYYY-MM-DD): ")
    if title == '':
        print "Please input a title for your new task"
        return
    task = dict()
    task['title'] = title
    if notes != '':
        task['notes'] = notes
    if due != '':
        task['due'] = due
    tasklist = tasklists['items'][list_num-1]
    tasklistID = tasklist['id']
    result = service.tasks().insert(tasklist=tasklistID, body=task).execute()
    print "[SUCCESS] The new task '" + result['title'] + "' has been created"


if __name__ == '__main__':
    json_data = readCredentials()
    authenticate(json_data)
    
    parser = argparse.ArgumentParser(description='A python CLI tool to manage your google tasks')
    parser.add_argument('-l', dest='lists', action='store_true', help='show all your tasklists names')
    parser.add_argument('-t', dest='tasks', action='store', metavar='NUMBER', nargs=1, type=int,
                        help='show all tasks in the specified task list')
    parser.add_argument('-N', dest='newList', action='store', metavar='TITLE', nargs=1, type=str,
                        help='create a new task list')
    parser.add_argument('-U', dest='updateList', action='store', metavar=('NUMBER', 'TITLE'), nargs=2,
                        help='update the specified task list with the new title')
    parser.add_argument('-D', dest='delList', action='store', metavar='NUMBER', nargs=1, type=int,
                        help='delete the specified task list')
    parser.add_argument('-n', dest='newTask', action='store', metavar='NUMBER', nargs=1, type=int,
                        help='create a new task on the specified task list')

    
    args = parser.parse_args()

    if args.lists:
        getTaskLists()
    elif args.tasks is not None:
        getTasks(args.tasks)
    elif args.newList is not None:
        createNewTaskList(args.newList)
    elif args.updateList is not None:
        updateTaskList(args.updateList)
    elif args.delList is not None:
        delTaskList(args.delList)
    elif args.newTask is not None:
        createNewTask(args.newTask)
