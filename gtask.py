#! /usr/bin/env python

import gflags
import httplib2
import json
import argparse
import os

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from colorama import init, Fore
init(autoreset=True)

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

    script_dir = os.path.dirname(__file__)
    rel_path = 'tasks.dat'
    abs_file_path = os.path.join(script_dir, rel_path)
    storage = Storage(abs_file_path)
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
    script_dir = os.path.dirname(__file__)
    rel_path = "credentials.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as f:
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
            print list_num, tasklist['title'] # print task list title
            for i, task in enumerate(tasks['items']):
                if 'completed' in task:
                    print ' ', i+1, Fore.GREEN + task['title']
                else:
                    print ' ', i+1, task['title']
        else:
            print "[WARNNING] The task list '" + tasklist['title'] + "' has not yet any tasks"

def getTask(opts):
    list_num, task_num = opts
    list_num = int(list_num)
    task_num = int(task_num)
    tasklists = service.tasklists().list().execute()
    if list_num > len(tasklists['items']) or list_num == 0:
        print "[ERROR] Please give a correct list number"
        return
    else:
        tasklist = tasklists['items'][list_num-1]
        tasklistID = tasklist['id']
        tasks = service.tasks().list(tasklist=tasklistID).execute()
        if task_num > len(tasks['items']) or task_num == 0:
            print "[ERROR] Please give a correct task number"
            return
        else:
            task = tasks['items'][task_num-1]
            print "Task: " + task['title']
            if 'due' in task:
                print "Due: " + task['due'][0:10]
            if 'notes' in task:
                print "Notes: " + task['notes']
            if 'completed' in task:
                print "Status: " + task['status']
                print "Completed: " + task['completed'][0:10] 

def createNewTaskList(list_title):
    new_tasklist = {
        'title': list_title
    }
    result = service.tasklists().insert(body=new_tasklist).execute()
    print "[SUCCESS] The new task list '" + result['title'] + "' has been created"

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
        task['due'] = due + 'T00:00:00.000Z'
    tasklist = tasklists['items'][list_num-1]
    tasklistID = tasklist['id']
    result = service.tasks().insert(tasklist=tasklistID, body=task).execute()
    print "[SUCCESS] The new task '" + result['title'] + "' has been created"

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
        return
    else:
        tasklist = tasklists['items'][list_num-1]
        tasklistID = tasklist['id']
        list_old_title = tasklist['title']
        service.tasklists().delete(tasklist=tasklistID).execute()
        print "[SUCCESS] The tast list '" + list_old_title + "' has been deleted"

def delTask(opts):
    list_num, task_num = opts
    list_num = int(list_num)
    task_num = int(task_num)
    tasklists = service.tasklists().list().execute()
    if list_num > len(tasklists['items']) or list_num == 0:
        print "[ERROR] Please give a correct list number"
        return
    else:
        tasklist = tasklists['items'][list_num-1]
        tasklistID = tasklist['id']
        tasks = service.tasks().list(tasklist=tasklistID).execute()
        if task_num > len(tasks['items']) or task_num == 0:
            print "[ERROR] Please give a correct task number"
            return
        else:
            task = tasks['items'][task_num-1]
            taskID = task['id']
            service.tasks().delete(tasklist=tasklistID, task=taskID).execute()
            print "[SUCCESS] The task '" + task['title'] + "' has been deleted"

def completeTask(opts):
    list_num, task_num = opts
    list_num = int(list_num)
    task_num = int(task_num)
    tasklists = service.tasklists().list().execute()
    if list_num > len(tasklists['items']) or list_num == 0:
        print "[ERROR] Please give a correct list number"
        return
    else:
        tasklist = tasklists['items'][list_num-1]
        tasklistID = tasklist['id']
        tasks = service.tasks().list(tasklist=tasklistID).execute()
        if task_num > len(tasks['items']) or task_num == 0:
            print "[ERROR] Please give a correct task number"
            return
        else:
            task = tasks['items'][task_num-1]
            taskID = task['id']
            task['status'] = 'completed'
            result = service.tasks().update(tasklist=tasklistID, task=taskID, body=task).execute()
            print "[SUCCESS] The task '" + task['title'] + "' is marked as completed"

def clearTaskList(opts):
    list_num = opts[0]
    tasklists = service.tasklists().list().execute()
    if list_num > len(tasklists['items']) or list_num == 0:
        print "[ERROR] Please give a correct list number"
        return
    else:
        tasklist = tasklists['items'][list_num-1]
        tasklistID = tasklist['id']
        service.tasks().clear(tasklist=tasklistID).execute()
        print "[SUCCESS] All the completed task in task list '" + tasklist['title'] + "' have been cleared"

if __name__ == '__main__':
    service = None
    json_data = readCredentials()
    authenticate(json_data)
    
    parser = argparse.ArgumentParser(description='A python CLI tool to manage your google tasks')
    parser.add_argument('-l', dest='lists', action='store_true', help='show all your task lists names')
    parser.add_argument('-t', dest='tasks', action='store', metavar='LIST_NUM', nargs=1, type=int,
                        help='show all tasks in the specified task list')
    parser.add_argument('-T', dest='task', action='store', metavar=('LIST_NUM', 'TASK_NUM'), nargs=2,
                        help='show the speified task')
    parser.add_argument('-N', dest='newList', action='store', metavar='TITLE', nargs=1, type=str,
                        help='create a new task list')
    parser.add_argument('-U', dest='updateList', action='store', metavar=('LIST_NUM', 'TITLE'), nargs=2,
                        help='update the specified task list with the new title')
    parser.add_argument('-D', dest='delList', action='store', metavar='LIST_NUM', nargs=1, type=int,
                        help='delete the specified task list')
    parser.add_argument('-n', dest='newTask', action='store', metavar='LIST_NUM', nargs=1, type=int,
                        help='create a new task on the specified task list')
    parser.add_argument('-d', dest='delTask', action='store', metavar=('LIST_NUM', 'TASK_NUM'), nargs=2,
                        help='delete the specified task from the task list')
    parser.add_argument('-c', dest='clearList', action='store', metavar='LIST_NUM', nargs=1, type=int,
                        help='clear all completed tasks from the specified task list')
    parser.add_argument('-m', dest='markTask', action='store', metavar=('LIST_NUM', 'TASK_NUM'), nargs=2,
                        help='mark the specified task as completed')

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
    elif args.delTask is not None:
        delTask(args.delTask)
    elif args.clearList is not None:
        clearTaskList(args.clearList)
    elif args.task is not None:
        getTask(args.task)
    elif args.markTask is not None:
        completeTask(args.markTask)
