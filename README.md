# Viva API Adapter - VADA

## Requirements

- Homebrew
- Python 3.7.7 or higher
- Pipenv

## Getting started

### Make sure [homebrew](https://brew.sh) is installed and up to date

```bash
brew update
brew upgrade
```

### Install pipenv

```bash
brew install pipenv
```

### Clone repo

```bash
git clone git@github.com:helsingborg-stad/helsingborg-viva-api-adapter.git
cd helsingborg-viva-api-adapter
```

### Setup python env

```bash
pipenv shell
pipenv install
```

### Set Envs

```bash
cp example.env .env
vi .env
export FLASK_ENV=development
export FLASK_DEBUG=true
export FLASK_APP=wsgi.py
```

### Run app

```bash
flask run
```
