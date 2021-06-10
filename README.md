# DOCUMENTATION

[Find documentation here](https://documenter.getpostman.com/view/5589548/TzeRpVPN).

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Arowne/pictsManager_2021_25.git
```

Then up the docker container by default the server is running on 0.0.0.0:80 (dependencies are automaticaly installed):

```sh
$ cd ./pictsManager_2021_25/app/
$ sudo docker-compose up -d
```
Running test:

```sh
$ cd ./pictsManager_2021_25/app/
$ sudo docker exec -it app_web_1 bash
$ python3 manage.py test
```
