# gTask-cli

## Description

[gTask-cli](https://github.com/yankuangshi/gTask-cli) is a simple python CLI tool to manage your Google Tasks. It uses the [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/) to interact with the [Google Tasks API](https://developers.google.com/google-apps/tasks/).

## Requirements

Requires Python 2.7 to run the script. It also needs the following dependencies:

* [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/)
* [argparse library](https://pypi.python.org/pypi/argparse)
* [colorama library](https://pypi.python.org/pypi/colorama)

## Installation

All of dependencies above can be installed with `pip`:

```
$ pip install --upgrade google-api-python-client
$ pip install argparse
$ pip install colorama
```
Before using the script, there are a few steps you need to follow to register your app as it needs to be authorized to make requests to google service.

*  Go to [Google APIs Console](https://console.developers.google.com) to create a new project.

*  Click `APIs` in the project pane and activate the `Google Tasks API` for your project. 

*  Click `Credentials` in the project pane, in `OAuth` section create a new client ID, choose `Installed application` as `APPLICATION TYPE`. It will generate a `client ID` and a `client secret` which will be used for our tool.

*  In `Public API access` section, create a new key. Choose `Server key` from the pop-up. This will generate an `API key` which will be used in our script.

Now you've finished registering your project.

* [Download](https://github.com/yankuangshi/gTask-cli/archive/master.zip) zip and unzip the project or use git clone to download it 

* Add the generated `client ID`, `client secret` and `API key` to the `credentials.json` file

* For running the script anywhere from the command line and without the python command :

  * Make the gtask.py file executable `$ chmod +x gtask.py`
  
  * Add the gTask-cli project directory to your `PATH` environment variable. In your `.bashrc` file, add `export PATH=/path/to/project/:$PATH` and then `source` your `.bashrc` file
  
  * To simplify your use of the script, I recommend to add an alias to the gtask.py file, like : `alias gtask='/path/to/project/gtask.py'`
   
**NOTE:** For the first time, There will be a dialogue to request you for the permission to access your google tasks data, just copy the generated url and paste it in a browser address bar and accept the access to your tasks data, then paste the provided key back into the terminal. The `tasks.dat` file will be generated.

**NOTE:** Remember that you should never commit the credentials.json and tasks.dat files to your github.

## Usage

For help, use `-h` option.

```
$ gtask -h
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

## Usage examples
* `-h` or `--help` : show the help message and exit
* `-l` : show all your tasklists names
  
  ```
  $ gtask.py -l
  1 - tasklist1
  2 - tasklist2
  ```
* `t LIST_NUM` : show all tasks in the specified task list
  
  ```
  $ gtask.py -t 1
  1 tasklist1
    1 Go to gym
    2 Finish the homework
    3 Finish the python project
  ```
* `-T LIST_NUM TASK_NUM` : show the specified task
  
  ```
  $ gtask.py -T 1 1 
  Task: Go to gym
  Due: 2014-07-25
  Notes: It has to be done!
  ```
* `-N TITLE` : create a new task list

  ```
  $ gtask.py -N "tasklist3"
  [SUCCESS] The new task list 'tasklist3' has been created
  $ gtask.py -l
  1 - tasklist1
  2 - tasklist2
  3 - tasklist3
  ```
* `-U LIST_NAME TITLE` : update the specified task list with the new title

  ```
  $ gtask.py -U 3 "new tasklist 3"
  [SUCCESS] Update the task list 'tasklist3' to 'new tasklist 3'
  $ gtask.py -l
  1 - tasklist1
  2 - tasklist2
  3 - new tasklist 3
  ```
* `-D LIST_NUM` : delete the specified task list

  ```
  $ gtask.py -D 3
  [SUCCESS] The tast list 'new tasklist 3' has been deleted
  ```
* `-n LIST_NUM` : create a new task on the specified task list

  ```
  $ gtask.py -n 1
  Task title: Do mont-blanc toor
  Task notes: during 7 days
  Task due (YYYY-MM-DD): 2014-08-16
  [SUCCESS] The new task 'Do mont-blanc toor' has been created
  ```
* `-d LIST_NUM TASK_NUM` : delete the specified task from the task list

  ```
  $ gtask.py -t 2
  2 tasklist2
    1 task sample 1
    2 task sample 2
  $ gtask.py -d 2 2
  [SUCCESS] The task 'task sample 2' has been deleted
  ```
* `-m LIST_NUM TASK_NUM` : mark the specified task as completed
* `-c LIST_NUM` : clear all completed tasks from the specified task list

  ```
  $ gtask.py -m 1 3
  [SUCCESS] The task 'Finish the homework' is marked as completed
  $ gtask.py -c 1
  [SUCCESS] All the completed task in task list 'tasklist1' have been cleared
  $ gtask.py -t 1
  1 tasklist1
    1 Do mont-blanc toor
    2 Go to gym
    3 Finish the python project
  ```

## You can help
Feel free to report errors or requests. Any contributions are welcomed. 

## License
gTask-cli is relesed under the MIT License.


  
