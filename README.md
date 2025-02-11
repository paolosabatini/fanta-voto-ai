# fanta-voto-ai
ML algorithm to estimate the vote for FantaWomen based on available data. More documentation in the dedicated [web-page](https://paolosabatini.github.io/fanta-voto-ai/).

This version `v2` is not documented in the webpage, as under development and completely new with respect to previous version. It is going to be documented once the project is mature enough.

## Setting up

### MySQL database local setup

Install `mysql` service

```shell
# MacOS
$ brew install mysql

# Start the service (change with restart to restart)
$ brew services start mysql

# To check the running services
$ brew services list
```

To access to the local database

````shell
mysql -u root -p
```

The setting up of the needed tables are in `config/db`. To set the database up:

````shell
cd ./config/db
mysql -u root -p < create_database.sql
mysql -u root -p < create_tables.sql

# To load the players, setup the local_infile in server
# mysql> SET GLOBAL local_infile=1
mysql -u root -p --local-infile=1 < load_players_table.sql

```

### Pyhon setup
Creation of the virtual environment

```shell
$ python3 -m venv $PWD/.venv
```

Activation and deactivation of the virtual environment

```shell
# activation
$ source .venv/bin/activate

# de-activation
$ deactivate
```

Install the needed modules

````shell
$ pip install bs4
$ pip install mysql-connector-python
$ pip install unidecode
$ pip install mysql-connector
$ pip install mysqlclient 
```

