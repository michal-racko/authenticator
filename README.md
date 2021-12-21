# Authenticator

Provides an OAuth2 authentication server and a user interface for account management. Please refer
to https://django-oauth-toolkit.readthedocs.io/en/latest/index.html for more information on how to register an app with
OAuth2 and use the authorization tokens.

## Settings

The microservice is configured using environment variables, or their Docker-secret alternatives
(see https://docs.docker.com/engine/swarm/secrets/ for more info):

- `AUTHENTICATOR_BASE_URL` / `AUTHENTICATOR_BASE_URL_FILE` - Base URL for the UI API. Default: `api/v1`.
- `AUTHENTICATOR_SECRET_KEY` / `AUTHENTICATOR_SECRET_KEY_FILE` - (required) Secret key for cryptographic purposes.
- `AUTHENTICATOR_ALLOWED_HOSTS` / `AUTHENTICATOR_ALLOWED_HOSTS_FILE` - A comma-separated list of allowed
  hosts (https://stackoverflow.com/questions/54504142/how-to-set-django-allowed-hosts). Default: `localhost`.
- `AUTHENTICATOR_OAUTH2_URL` / `AUTHENTICATOR_OAUTH2_URL_FILE` - Base URL for the OAuth2 server.
  Default: `http://localhost:8000/o`.
- `AUTHENTICATOR_ADMIN_USERNAME` / `AUTHENTICATOR_ADMIN_USERNAME_FILE` - (required) Admin username
- `AUTHENTICATOR_ADMIN_EMAIL` / `AUTHENTICATOR_ADMIN_EMAIL_FILE` - (required) Admin email
- `AUTHENTICATOR_ADMIN_PASSWORD` / `AUTHENTICATOR_ADMIN_PASSWORD_FILE` - (required) Admin password
- `AUTHENTICATOR_DEBUG` - Whether to use debug mode (make sure it's set to False when in production).

## Run

The corresponding Docker will serve the application on port 8000. Make sure the port is exposed and properly forwarded.

## Register your microservice

A user who completes login in one of the applications registered with the authentication server will have access to
all other registered applications using their access token. To register your microservice do the following:

- Login to the admin page `<authenticator-url>/admin/` (or ask your admin to do this)
- Go to the application site: `<oauth2-url>/applications/`
- Click on the `New Application` button
- Fill in the form (see https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html for more details)
- Save & use your application's `client_id` and `client_secret` (
  see https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-4-get-your-token-and-use-your-api)

## Tests

Make sure to run migrations first:

- `cd src`
- `python manage.py migrate`
- `python manage.py test user_interface`