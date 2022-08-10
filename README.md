# Flask Demo Project

https://flask.palletsprojects.com/en/2.1.x/tutorial/

## Setup

### Windows

From elevated PowerShell

1. `Set-ExecutionPolicy RemoteSigned` allow own scripts and trusted third parties
2. `scripts\windows\install` installs venv and flask
3. `scripts\windows\activate`  activates venv and sets environment variables for running the application
4. `flask init-db` drops current database and creates new one with correct schema
5. `flask run`

Run `pip install -e .` from directory where setup.py is to install program as pip module --> 