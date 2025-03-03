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
Need to change on server side as well
```
mysql>SET GLOBAL local_infile=1
```

If you have issues with password login in `mysql 9.0`, the correct instructions to downgrade to `8,4` are ![here|https://github.com/Homebrew/homebrew-core/issues/180498#issuecomment-2296006936]

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
$ pip install pandas
$ pip install numpy
$ pip install matplotlib
```


## 🚀 Installing Metabase with Docker on macOS

### **1. Install and Run Metabase with Docker**

1. **Install Docker** (if not installed):
   ```sh
   brew install --cask docker
   open -a Docker
   docker --version
   ```

2. **Pull and Run Metabase**:
   ```sh
   docker pull metabase/metabase
   docker run -d -p 3000:3000 --name metabase metabase/metabase
   ```

3. **Access Metabase**:
   - Open **[http://localhost:3000](http://localhost:3000)** in a browser.

4. **Manage Metabase**:
   ```sh
   docker stop metabase   # Stop Metabase
   docker start metabase  # Restart Metabase
   docker logs -f metabase  # View logs
   docker rm -f metabase  # Remove container
   ```

### **2. Connect Metabase to a Local Database**

1. **Ensure your database (e.g., MySQL, PostgreSQL) is running**:
   ```sh
   brew services start mysql@8.4  # Example for MySQL
   ```

2. **Find your local machine's IP address for Docker**:
   ```sh
   docker network inspect bridge | grep Gateway
   ```
   Use the **Gateway IP** (e.g., `192.168.1.X`) instead of `localhost` when configuring the database connection in Metabase.

3. **Add the database in Metabase**:
   - Go to **Admin > Databases > Add Database**
   - Enter database details:
     - **Host**: Use the IP found in step 2
     - **Port**: 3306 (for MySQL) or 5432 (for PostgreSQL)
     - **Username & Password**: Your database credentials

4. **Test the connection and save.** 🎉

Metabase is now installed and connected to a local database on macOS! 🚀

