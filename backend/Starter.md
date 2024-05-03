
# Backend Starter Guide

This small guide is created for setting up development environment on your machine after cloning repo from github. Note that this guide applies to MONOLITHIC version of the project. If current version is microservice, significant differences may be present.

## 1 Virtual environment
If you are reading this, it means you have probably already forked and cloned the repository to your machine. Next step is to create a "virtual environment" which will allow you to download dependencies for the project without effecting your entire system. Open a new terminal window in roster_generator_website and execute fallowing commands in order:

```shell
python -m venv venv
venv\scripts\activate
source venv/bin/activate
pip install -r website/requirements.txt
```
First three commands steup and activate environment, while the last one installs dependencies (which are listed in requirements.txt).

## 2 Environment variables

TL;DR You need to create file named .env inside website folder, it will stay empty for now.

Often times there are special pieces of information we need to give our program to configure it. This can be things such as location of a backup file, username and password for connection to a service ect. One way (not an ideal one from secuirty perspective but sufficent for this project) is environment variables. We can place key-value pairs to .env file and then read them from our program. A very important thing to note is that, since this file will oftentimes contains things like passwords, keys ect. it is considered a "secret" file (and management of this data is refered as "secret management") and it should NEVER be pushed to github. Therefore your repository currently does not have a .env file. Create one in website directory. Make sure name is exactly .env

## 3 Setup PostgresSQL

We now need to start our postgres server, so that our web server can create and use database functionalities. First, start by downloading PostgreSQL and phppgadmin which we will use to access the databse with web gui.

```shell
su root
sudo install postgresql postgresql-client
sudo apt install phppgadmin
```

Then we can start the postgres server. After server starts, login to admin account with second command.

```shell
sudo systemctl start postgresql
sudo -u postgres psql
```

Then we want to create a new database user which will be used by our web server to connect to postgres. We also have to give it permission to create new databases. (you can randomly choose username and password) (last command logouts from postgres)

```shell
CREATE USER username WITH PASSWORD 'password';
ALTER USER username CREATEDB;
\q
```

Now before moving to subsequent steps, make sure to add credidentials of this user to .env file so that our flask server will be able to access them. Add fallowing line to .env (with username password you have defined)

```
DATABASE_PROG=postgresql
DATABASE_HOST=localhost
DATABASE_USERNAME=username
DATABASE_PASSWORD=password
```

Then go to "http://localhost/phppgadmin/" to access control panel. Click on "PostgreSQL" (under phpPgAdmin, top left) to open login. Then enter your username and password to login. (check next paragraph if you can't) Click on "Create database". Write "FlightRosterDb_Mono" as db name and select UTF8 from dropdown menu for encoding and press create.

While logging in to db user, I initially recived an error message regarding faliure of peer authentication. This error can be solved by fallowing instructions in "https://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge". You basically have to change peer statements to md5.

Note: file path on my machine is "/etc/postgresql/13/main/pg_hba.conf".

Last step is to create tables in DB that will be used by our server. For this purpose, we will use a special script "InitDB.py". This script basically connects to DB using information in .env file, then creates tables for models defined under Models directory. Execute InitDB.py, then check if tables are created from phpPGAdmin.

## 4 Executing server and testing with CURL

Normally to execute a python script file, you would just use python *filename*. However this aproach is only used to execute small scripts and what we want to do here is module execution which will execute are project from a well defined entry point, which is the main file. To execute project this way open terminal in roster_generator_website folder and use fallowing command:

```shell
python -m website
```

This will execute "website" (which is our backend project) as a module, starting execution by running main file. Our server is now runing and listening on http requests from a specific port (it will probbaliy be 5000, you can check main, if no port is specfied in main, add "PORT=5000" to .env)

We can test our server by sending it a http request and checking for result. CURL is a command line program that can do that. Open a new terminal window and execute fallowing curl command: (you may have to correct the port number if it has changed)

```shell
curl http://127.0.0.1:5000/
```

If you are getting something like "idrava was here" ect. as output in terminal and no error messages it should be working.