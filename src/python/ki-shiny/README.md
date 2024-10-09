# white duck azure open ai template
A small shiny app with semantic kernel interacting with AzureOpenAi

## Description

This template provides boilerplate for a small shiny application, with everything needed to get going quickly.

- complete implementation of a semantic-kernel flow
- chat with context
- agent chat
- deployment via docker
- quick run powershell and bash script
- vscode settings for debugging and formatting
- Classic modular service-based app architecture/structure
- Dependency Injection Container
- Appsettings support
- logging preconfigured

## Requirements

- **python >= 3.10**
- **poetry**: https://python-poetry.org/docs/#installation

`setup_and_run`scripts will install poetry

## Libraries Used

Following libraries are part of this template

- **Shiny package**: `shiny`, `shinyswatch`, `shiny-validate`, `shinywidgets` for all things shiny
- **loguru**: Logging
- **pendulum**: Datetime handling without insanity
- **python-decouple**: Appsettings
- **pandas**: Dateframes and tables

Following libraries are getting installed as dev environment

- **ruff**: Linting, formatting, all in one
- **pytest**: Test framework


## Run

a) Open in VSCode Press `F5`

b) `python app.py`

c) Run `setup_and_run.ps1` or `setup_and_run.sh`

## Static web app

Because why not, shiny apps are also deployable as static web sites on servers that don't even have python support.

BUT supports not all python packages!
See this list:

https://shiny.posit.co/py/docs/shinylive.html

Export static website with shinylive

```
shinylive export . site
```

Host with IIS or your favorite http-server

```
python3 -m http.server --directory site 8008
```

## Docker


### Local Docker

c) Run `setup_and_run.ps1 -useDocker` or `setup_and_run.sh --useDocker`

or

```
docker build -t whiteduck .
docker run --rm -p 8000:8000 whiteduck
```

### Deploy to Azure Container Registry

#### Login
```
az login
az account set --subscription xxx
```

#### Create ACR
```
az acr create --resource-group MY_RESSOURCE_GROUP --name WHITEDUCK --sku Basic
```

#### Login to ACR
```
az acr login -n WHITEDUCK
```

#### Tag and Push
```
docker build -t whiteduck .
docker tag whiteduck whiteduck.azurecr.io/whiteduck:latest
docker push whiteduck.azurecr.io/whiteduck:latest
```
