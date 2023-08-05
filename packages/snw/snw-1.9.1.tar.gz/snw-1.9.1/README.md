This project is based on github nmt-wizard as a sub-module and brings additional functionalities to the project.

`systran-nmt-wizard` implements:
- a new client `client/launcher.py`
- a new server `server/main.py`

The worker stays the same. To use these new modules, the `PYTHONPATH` variable should be set to:

* `${NMT_WIZARD_PATH}/server` to launch the rest server through flask
* `${NMT_WIZARD_PATH}/client` to launch the client application

## Configuration file
The configuration file setting for both worker and rest server should be the same and are taken from `LAUNCHER_CONFIG` variable.

THe default `setting.ini` in `server` directory has the following format:
```
[flask]
debug = false

# SYSTRAN NMT WIZARD extensions
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI=sqlite:////tmp/test.db
SECRET_KEY='Super secret key'

[default]
# config_dir with service configuration
config_dir = ./config
# logging level
log_level = DEBUG
# refresh counter (in 1/100 of seconds)
refresh_counter = 200
# quarantine time (in s)
quarantine_time = 600

[redis]
host = localhost
port = 6379
db   = 0
#redis_password=xxx
```

The `SQLACHEMY` configuration block configures the database used by Flask through `flask-SQLAlchemy` (see [here](http://flask-sqlalchemy.pocoo.org/2.3/config/) for more details.

To create the DB and a user - one can use the following python code (from server directory):

```
from lib.models import db, User

db.create_all()
jean=User('jean','SAJAS','007')
db.session.add(jean)
db.session.commit()
```

## Authentication

Requests to the mmt-wizard REST server requires an authentication from the user. The authentication is created with the new route: `/auth/tok` and the header of the request contains HTTP authentication such as:

```
$ curl -i  -u SAJAS:007 -X GET http://127.0.0.1:5000/auth/token
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 160
Server: Werkzeug/0.14.1 Python/2.7.10
Date: Mon, 09 Apr 2018 13:21:26 GMT

{
  "duration": 600, 
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUyMzI4MDY4NiwiaWF0IjoxNTIzMjgwMDg2fQ.eyJpZCI6MX0.gZwQk1U8hSESewywr-eoC2pydDt6cYSq1t5sSRCcPg0"
}
```

Through the client, the new `login` command performs the same call and save the token in `${HOME}/.launcher_token`.

```
$ python client/launcher.py login
Login: SAJAS
Password: 
INFO:root:Got token (_T_eyJhbGciOiJIUzI1NiIsImV4cCI6MTUyMzI4MDg2MSwiaWF0IjoxNTIzMjgwMjYxfQ.eyJpZCI6MX0.MHL5Lqv8ACvXxW1ZHVO-VHwvYQ5IV6zt9zEReKa4Nl8) for 600s
```

For all other commands, the token is sent seamlessly to the server along with the request and will be used to check on user access rights.

2 types of tokens exist and are identified by their 3 first letters as described followed. Tokens are identifying a user for a given duration, and might be restricted to a specific task.

- `_T_` temporary tokens: these tokens are saved in redis database as `token:TOKEN` keys. Value of the redis entry is the *restriction*.
- `_P_`persistent tokens: these tokens are saved in SQL database

## Permission

User permission schema is described here:

![db schema](./misc/user_db_schema.png)

and involves different concepts:

* *Abilities*: assigning permission to performed tasks
* *Roles*: a role is a collection of abilities
* *Entities*: entities are formal entities regrouping users and pools. The first 2 letters of users `trainer_id` and pools names are the entities and condition all assigned permissions. 

Permissions for the different actions are associated to `abilities`. A role is a collection of abilities.

| ABILITY     | Description |
| ---         | --- |
| `edit:user` | Edit user list |
| `edit:user:ROLE` | Edit/Add/Delete user list with ROLE level |
| `config:user:ROLE` | Edit/Add/Delete user list with ROLE level |
| `del:user` | Remove a user - conditioned to `edit:user:ROLE` |
| `del:model` | Delete a model |
| `terminate:*` | terminate a task from another user |
| `terminate:self` | terminate a task from oneself |
| `train` | launch a task |

The different roles are:
* `super`: `del:user`, `edit:user`, `edit:user:*`
* `admin`: `edit:config`, `edit:user:lingadmin`, `edit:user:trainer`, `edit:user`, `terminate:*`
* `lingadmin`: `terminate:*`; `del:model`, `train`
* `trainer`: `train`
* `user`: none

Each role can be attached to a specific entity: hence a user with `SA:lingadmin` permission can only perform `lingadmin` tasks assigned to `SA` users or pools. `*` entity covers all of the entities. The highest role to a user is `*:super`.

## Setting up development environment

A docker compose file is provided to set-up a clean development environment configured with 2 pool - a real server `demogpu02`, and a /fake test server/ `remote_test` simulating a 4 node GPU server.

* run some local "remote hosts":
```
docker-compose -f dockers/docker-compose-dev.yml  up --build
```

* launch workers:
```
cd dockers/config-dev/
nohup python ../../nmt-wizard/server/runworker.py remote_test_pool >> runworker.log &
nohup python ../../nmt-wizard/server/runworker.py demogpu02 >> runworker.log &
nohup python ../../nmt-wizard/server/runworker.py cpu_server_pool >> runworker.log &
```

* launch development launcher:
```
cd dockers/config-dev/
export PYTHONPATH=${PWD}/../../nmt-wizard/server
export LAUNCHER_CONFIG=${PWD}/settings.ini
FLASK_APP=../../server/main.py flask run
```

* create user database if not existing
```
export PYTHONPATH=${PWD}/server:${PWD}/nmt-wizard/server
export LAUNCHER_CONFIG=${PWD}/dockers/config-dev/settings.ini
python scripts/create.py 
```

* run snw:
```
export SNW_URL=http://localhost:5000
export PYTHONPATH=${PWD}/nmt-wizard
python client/snw ls
```

should display:
```
+--------------------------+-------+--------+----------+------+------------------------+
| Service Name             | Usage | Queued | Capacity | Busy | Description            |
+--------------------------+-------+--------+----------+------+------------------------+
| cpu_server_pool [38627]  | 0 (0) |   1    |  0 (4)   |  1   | test local environment |
| remote_test_pool [38627] | 0 (0) |   0    |  6 (13)  |  0   | test local environment |
| demogpu02 [38627]        | 0 (0) |   0    |  1 (2)   |  0   | gpu test server        |
+--------------------------+-------+--------+----------+------+------------------------+
```

## Testing

A full environment can be set with the following docker-compose

* offline configuration (without AWS services)
```
rm -f dockers/config-test/logs/log-* ; rm -f dockers/config-test/*pool.json ; rm -rf tests/models/*

docker build -t systran/snw_launcher:dev -f dockers/launcher/Dockerfile .
docker build -t systran/snw_worker:dev -f dockers/worker/Dockerfile .

docker-compose -f dockers/docker-compose-test.yml  build [--no-cache]
docker-compose -f dockers/docker-compose-test.yml  up -V
pytest --variable tests/dev-test.json tests [--online]
```

* online configuration (with AWS services)
```
rm -f /tmp/snw_{logs,taskfiles}/* ; rm -f dockers/config-test*/*pool.json ; rm -rf tests/models/*

docker build -t systran/snw_launcher:dev -f dockers/launcher/Dockerfile .
docker build -t systran/snw_worker:dev -f dockers/worker/Dockerfile .

docker-compose -f dockers/docker-compose-test-aws.yml  build [--no-cache]
docker-compose -f dockers/docker-compose-test-aws.yml  up -V
pytest --variable tests/dev-test.json tests [--online]
```
