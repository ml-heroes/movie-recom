[Colab Jupyter Notebook](https://colab.research.google.com/github/ml-heroes/movie-recom/blob/master/ml/movie-recom.ipynb)

# Netflix-Like Movie Recommendation System

### Machine Learning Platform to recommend movies to users based on trending-movies and users movie-history.

The project has the following key features:

- The project structure supports multiple development environments with the usage of `.env`
  variable and `docker.compose.yml` files.
- Designed for organizing large scale application structure. With the usage of `Blueprints`,
  `application factory` and different configs, you can easily extend this seed project to any
  Production ready application.
- `Service` Class that encapsulates common SQLAlchemy operations to interact with data model by
  exposing APIs.
- Support Flask code Testing out of the box. For commands to test, see below.
- Reverse proxy using `nginx`.

It is built with following components:

- React - Frontend framework.
- Flask(1.1.2) - Micro web framework (Python-3.6.2) for the backend.
- nginx - web server (It's also used for reverse proxy). External user hits the nginx which distributes the request between Frontend and Backend using url.
- uwsgi - It's a WSGI server that help running web application written in Python. It comes with direct support for popular NGINX web server.
- Docker - Usage of Docker Compose to build and host the application.

## Project Components (Directory Structure)

### client

This directory holds the React code.

### nginx

This directory holds the nginx config file and Dockerfile for running the nginx container. This container serves the Angular code and also passes request to backend.

### server

This directory contains the server side code. It hosts the **Flask** app, **tests** setup and
other configs and settings files required by the backend. It also has Dockerfile for running the
flask container. This container hosts the backend code.

### Environment variable

A simple `.env` file to set the environment variables for Flask and Postgres. We can have multiple
versions of this file for different environments.

### docker-compose.yml

This file is used by the Docker to create the containers and run your app. We can have multiple
versions of this file for different environments.

## Architecture

For this seed project, I am using 3 Docker containers:

- NGINX - Web Server
- FLASK - Flask web application with _uwsgi_ server.

The three components are all created from Docker images that expand on the respective official
images from Docker Hub. Each of these images are built using separate Dockerfiles. Docker Compose
is then used to create all three containers and connect them correctly into a unified application.

### Working

The request from an external user hits the _nginx_ web server on port 80. Depending on the
**URL**,the request is served using Angular code or it is sent to Flask web application. In this
app, all request URL starting with _/api_ is sent to Flask web service. The Flask docker
container is also running and it exposes port 5000. These setting are defined in _nginx.conf_
file. In this way, nginx is aware of both Frontend and Backend services. The Flask container
talks to the PostgreSQL database on port 5432 for any request that require database operations.

## Usage

**NOTE**: Make sure you have Docker, node, npm and angular-cli installed. Check Angular
Prerequisites [here](https://github.com/angular/angular-cli#prerequisites).

- Clone this repository
- **Not Required** - Navigate to client directory and execute `yarn build` to create production build for Angular.
- Then navigate back and execute following commands:
  - `docker-compose build`
  - `docker-compose up`
  - _OR_ just run one command: `docker-compose -f docker-compose.yml up --build`
- Open Browser and type following URL:
- `localhost` - It should display the Welcome message from Angular and a default message from
  backend.
- `localhost/api` - It should display welcome message from Flask.
- `localhost/api/ping` - To get a `json` from Flask.

This seed project is good for starting up with any Angular-Flask-Docker project, so check it out and feel free to fork, update, plug in your project etc. Let me know if you find any issues.

## References

Starter Project From: https://github.com/mrsan22/Angular-Flask-Docker-Skeleton

UI Starter Project From: https://github.com/AndresXI/Netflix-Clone
