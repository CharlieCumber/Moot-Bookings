# Moot Bookings App

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

You will need to follow the instructions ['Raw Token Requests']('https://smartsheet-platform.github.io/api-docs/#raw-token-requests') to generate an access token for SmartSheets. You will need to set the SMARTSHEET_ACCESS_TOKEN config variable in your .env file to this value.

## Running the App

### Option 1: Docker

Docker compose configurations are provided for both production and development modes. The production configuration uses Gunicorn, while the development configuration uses Flask development server which has the additional benifit of hot reloading. You will need to have docker installed locally to use this option. You can istall docker [here]('https://docs.docker.com/get-docker/')

To start the application within a docker container, firstly ensure you have docker desktop installed and running, then you can run either command from your terminal:

```bash
# Production Mode
$ docker-compose up
```
```bash
# Development Mode
$ docker-compose -f docker-compose.development.yml up
```

### Option 2: Poetry

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Deployment

Travis CI is used to provide a continuous delivery of changes to the [deployed application on heroku]('https://moot-bookings.herokuapp.com/').
The pipeline builds a docker image of the production configured application and pushes the image to the heroku image repository for release.

### Manual Deployment

You can manually deploy the application from the terminal, but note this deployment will be overwritten should the automatic deployment pipline be triggered by a commit to master.
Before running the code below, ensure you have docker desktop running.

Firstly, get the heroku api key and set it as an enviroment variable. Then you will be able to log into the heroku docker image repository:
```bash
$ HEROKU_API_KEY=api_key_from_heroku_settings_page_here
$ echo "$HEROKU_API_KEY" | docker login --username=_ --password-stdin registry.heroku.com
```

Secondly, build and push the image to the heroku image repository:
```bash
$ docker build --target production --tag moot-app .
$ docker image tag moot-app registry.heroku.com/moot-bookings/web
$ docker push registry.heroku.com/moot-bookings/web
```

Finally, trigger the release of the image and the replacement of the deployed application version:
```bash
$ heroku container:release web -a moot-bookings
```
