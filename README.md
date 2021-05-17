# DataBase compare tool #

Database comparsion tool made in python3

The tool is developed to compare 2 databases

It also has a search and replace function, that will search for a value in all tables and text columns of the database.
```
usage: dbcomparer.py [-h] -db1 DB1 [-db2 DB2] [-s S] [-r R] [-o O]

optional arguments:
  -h, --help  show this help message and exit
  -db1 DB1    Config file path for the database 1
  -db2 DB2    Config file path for the database 2
  -s S        Search string
  -r R        Replace string
  -o O        OutputFilePath

./dbcomparer.py -db1 /etc/mysql/db1.cnf -db2 /etc/mysql/db2.cnf
./dbcomparer.py -db1 /etc/mysql/db1.cnf -s searchvalue -r replacevalue
```

# What is in this repo #

#### Tool related things ####
The **src** folder contains all the source

The **dbcomparer.py** is the executable file

The **requeriments.txt** is the file to install dependencies with pip
```
pip3 -r install requeriments.txt
```

#### Developmennt related thing #####
Also there is a bunch of things to help in the development of the tool.

The **dockerdb1**,**dockerdb2** folders conain the necesary to start 2 mysql-databases

The **db1.cnf**,**db2.cnf**  contains the configuration parameters to connect the database instances

And finnally there is a script **start_devenv.sh** that automatically starts the docker containers
```
./start_devenv.sh
```

## Dependencies ##

- Python3-slack only if you want slack integration
- Python3-mysql-connector

### Exit codes cheatsheet ###
- 1 -> dbconnectionerror
- 2 -> Wrong parameters


# TO-DO list #

* [ ] Add support to more databases(postgre,sqlite)
* [X] Make the output report better, probably with html
* [X] Improve argument parsing
* [X] New feature, search and replace values in all database
* [X] New option, -o to chose a filepath and or filename to the report