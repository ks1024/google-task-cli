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
  -l                    show all your task lists names
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
* `-h` or `--help` : show the help message and exit
* `-l` : show all your tasklists names
  
  ```
  kuangshis-air:gTask kyan$ ./gtask.py -l
  1 - tasklist1
  2 - tasklist2
  ```
* `t LIST_NUM` : show all tasks in the specified task list
  
  ```
  kuangshis-air:gTask kyan$ ./gtask.py -t 1
  1 tasklist1
    1 Go to gym
    2 Finish the homework
    3 Finish the python project
  ```
* `-T LIST_NUM TASK_NUM` : show the specified task
  
  ```
  kuangshis-air:gTask kyan$ ./gtask.py -T 1 1 
  Task: Go to gym
  Due: 2014-07-25
  Notes: It has to be done!
  ```
* `-N TITLE` : create a new task list

  ```
  kuangshis-air:gTask kyan$ ./gtask.py -N "tasklist3"
  [SUCCESS] The new task list 'tasklist3' has been created
  kuangshis-air:gTask kyan$ ./gtask.py -l
  1 - tasklist1
  2 - tasklist2
  3 - tasklist3
  ```
* `-U LIST_NAME TITLE` : update the specified task list with the new title

  ```
  kuangshis-air:gTask kyan$ ./gtask.py -U 3 "new tasklist 3"
  [SUCCESS] Update the task list 'tasklist3' to 'new tasklist 3'
  kuangshis-air:gTask kyan$ ./gtask.py -l
  1 - tasklist1
  2 - tasklist2
  3 - new tasklist 3
  ```
* `-D LIST_NUM` : delete the specified task list

  ```
  kuangshis-air:gTask kyan$ ./gtask.py -D 3
  [SUCCESS] The tast list 'new tasklist 3' has been deleted
  ```
* `-n LIST_NUM` : create a new task on the specified task list

  ```
  kuangshis-air:gTask kyan$ ./gtask.py -n 1
  Task title: Do mont-blanc toor
  Task notes: during 7 days
  Task due (YYYY-MM-DD): 2014-08-16
  [SUCCESS] The new task 'Do mont-blanc toor' has been created
  ```
* `-d LIST_NUM TASK_NUM` : delete the specified task from the task list

  ```
  kuangshis-air:gTask kyan$ ./gtask.py -t 2
  2 tasklist2
    1 task sample 1
    2 task sample 2
  kuangshis-air:gTask kyan$ ./gtask.py -d 2 2
  [SUCCESS] The task 'task sample 2' has been deleted
  ```
* `-m LIST_NUM TASK_NUM` : mark the specified task as completed
* `-c LIST_NUM` : clear all completed tasks from the specified task list

  ```
  kuangshis-air:gTask kyan$ ./gtask.py -m 1 3
  [SUCCESS] The task 'Finish the homework' is marked as completed
  kuangshis-air:gTask kyan$ ./gtask.py -c 1
  [SUCCESS] All the completed task in task list 'tasklist1' have been cleared
  kuangshis-air:gTask kyan$ ./gtask.py -t 1
  1 tasklist1
    1 Do mont-blanc toor
    2 Go to gym
    3 Finish the python project
  ```
  

  