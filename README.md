Greenhouse Manager
===================
A conceptual inventory management web app geared towards greenhouse operators and the horticulturally inclined. The basic accounting functionalities of an inventory management system are paired with a local plant taxonomy database with the intent of complimenting and extending the functionality of the system.

The app was built off of the [flask-base](https://github.com/hack4impact/flask-base) project for developing the user interface, which uses Python3 (Flask) for creating the views and SQLAlchemy to connect to a DBMS. Refer to their documentation for more information about the software used and getting set up. 

On the server side, Greenhouse Manager was developed and deployed on a Raspberry Pi 4 with 1 GB RAM, quad-core Cortex-A72 SoC running at 1.5GHz, which was more than adequate. All of the software required should be readily available for Windows, macOS, Linux, and Unix systems, so any computer with Python3 installed and a stable internet connection should suffice. At least 1 GB RAM (or more) and ideally a dual-core (or more) processor are highly recommended. The web app utilizes HTML5, CSS, and JavaScript for rendering, so most any device that supports a modern web browser should be compatible. Since both retail and agricultural fields are very "hands-on," thought was put into making all of the features accessible from mobile devices but not all features have been fully tested yet.

## Setup

Starting with a fresh installation of [DietPi](https://dietpi.com/)(Raspbian), Python3 and Git are assumed to be installed, but just in case:

```shell
apt install python3 python3-pip git
``` 

Clone this repository 
```shell
git clone https://github.com/rinkekj/greenhouse-manager.git
```

Setup a virtual environment inside the project folder
```shell
python3 -m venv venv
source venv/bin/activate
```

Create a local config file and generate a SECRET_KEY variable
```shell
touch config.env
python3 -c "import secrets; print(secrets.token_hex(16))"
```

Paste key as SECRET_KEY in config.env
```
SECRET_KEY=THE_KEY_YOU_JUST_GENERATED
```

Install Python dependencies
```shell
pip install -r requirements.txt
```

Install Redis and SASS 
```shell
apt install redis-server sass
```

MariaDB
```shell
apt-install mariadb
```

Create User, Password, and Database in MariaDB
```shell
mysql -e "CREATE DATABASE plantDB;"
mysql -e "USER 'user'@'localhost' IDENTIFIED BY 'password';"
mysql -e "GRANT FILE ON *.* TO 'user'@'localhost';"
```

With the new user and password, define connectors in config.env to allow Greenhouse Manager to connect to the database
```
TEST_DATABASE_URL=mysql+mysqldb://user:password@localhost/plantDB
DATABASE_URL=mysql+mysqldb://user:password@localhost/plantDB
DEV_DATABASE_URL=mysql+mysqldb://user:password@localhost/plantDB
```

For demonstration purposes, run init_database.sh to finish setup and run a short simulation to fill the database with fake data
```shell
chmod +x init_database.sh
./init_database.sh
```

Otherwise, run the following to finish setup without adding any data
```shell
python manage.py recreate_db
python manage.py setup_dev
```

Finally, run the following to start the server and begin using Greenhouse Manager
```shell
source env/bin/activate
honcho start -e config.env -f Local
```
By default, the server is accessible over the local network through port 5000. One administrator account is added automatically during setup, so one can log in using 
```
Email:      admin@greenhouse.com
Password:   password 
```

Please refer to the [flask-base documentation](http://hack4impact.github.io/flask-base/) for more detailed instructions.

