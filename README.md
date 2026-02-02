# taskero_be

Project Management Software

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

#### Build docker

`docker compose -f docker-compose.local.yml build`

#### Start server

`docker compose -f docker-compose.local.yml up`

#### Migrations

`docker compose -f docker-compose.local.yml run django python manage.py makemigrations`

`docker compose -f docker-compose.local.yml run django python manage.py migrate`


#### Create superuser

`docker compose -f docker-compose.local.yml run django python manage.py createsuperuser`


## Creating your first tenant
- Log into django admin on `http://localhost:8000/admin` using credentials you created
- Find the tenant and domain models. If you create a tenant named `test` create domain as `test.localhost`
- Create tenant-superuser using following command:
    `docker compose -f docker-compose.local.yml run django python manage.py create_tenant_superuser`

### Verify your tenant-superuser
- Go to `http://test.localhost:8000/api/docs` for swagger UI
- Find the `/api/auth/login/` API endpoint
- Hit the endpoint using the tenant-superuser you created.

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
