# budget-management-backend
A Django Backend app to create, manage and view user budgets

## Start Django Project Commands:
```bash
python3 -m django --version
django-admin startproject budget_server
cd budget_server
python3 manage.py startapp user
```

## Database Setup Commands:
```bash
CREATE DATABASE budget_db;
CREATE USER budget_user WITH PASSWORD 'budget1234';
ALTER ROLE budget_user SET client_encoding TO 'utf8';
ALTER ROLE budget_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE budget_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE budget_db TO budget_user;


## Create Python Virtual Env:
```bash
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
virtualenv -p python3 budget-env
source budget-env/bin/activate
```

## Initial Setup to start server:
```bash
mkdir budget_server/logs
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
```