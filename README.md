# gTask

gTask is a python CLI tool to manage your Google Tasks

## Usage
For help, use `-h`option.

```
usage: gtask.py [-h] [-l] [-t LIST_NUM] [-T LIST_NUM TASK_NUM] [-N TITLE]
                [-U LIST_NUM TITLE] [-D LIST_NUM] [-n LIST_NUM]
                [-d LIST_NUM TASK_NUM] [-c LIST_NUM] [-m LIST_NUM TASK_NUM]

A python CLI tool to manage your google tasks

optional arguments:
  -h, --help            show this help message and exit
  -l                    show all your tasklists names
  -t LIST_NUM           show all tasks in the specified task list
  -T LIST_NUM TASK_NUM  show the speified task
  -N TITLE              create a new task list
  -U LIST_NUM TITLE     update the specified task list with the new title
  -D LIST_NUM           delete the specified task list
  -n LIST_NUM           create a new task on the specified task list
  -d LIST_NUM TASK_NUM  delete the specified task from the task list
  -c LIST_NUM           clear all completed tasks from the specified task list
  -m LIST_NUM TASK_NUM  mark the specified task as completed
```
