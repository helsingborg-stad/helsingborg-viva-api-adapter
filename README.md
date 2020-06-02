# Viva API Adapter - VADA

## Requirements

- Homebrew
- Python 3.7.7
- Pipenv

## Getting started

### Make sure [homebrew](https://brew.sh) is installed and up to date:
```
$ brew update
$ brew upgrade
```

### Install pipenv
```
$ brew install pipenv
```

### Clone repo
```
$ git clone git@github.com:helsingborg-stad/helsingborg-viva-api-adapter.git
$ cd helsingborg-viva-api-adapter
```

### Setup python env
```
$ pipenv shell
$ pipenv install
```

### Set Envs
```
$ cp example.env .env
$ vi .env
$ export FLASK_ENV=development
$ export FLASK_APP=wsgi.py
```

### Run app
```
$ flask run
```
