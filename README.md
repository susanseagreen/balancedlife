# Python: Getting Started
import django_heroku
Then add the following to the bottom of settings.py:

# Activate Django-Heroku.
django_heroku.settings(locals())

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.9 [installed locally](https://docs.python-guide.org/starting/installation/). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/heroku/python-getting-started.git
$ cd python-getting-started

$ python3 -m venv getting-started
$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local web -f Procfile.windows

heroku run python manage.py migrate

git push heroku main


```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku git:remote -a balancedlife

$ git push heroku main

$ heroku run python manage.py migrate

$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

```sh
https://stackoverflow.com/questions/36665889/collectstatic-error-while-deploying-django-app-to-heroku
## disable the collectstatic during a deploy
$  heroku config:set DISABLE_COLLECTSTATIC=1
## deploy
$  git push heroku main
$  heroku ps:scale web=1
## run migrations (django 1.10 added at least one)
$  heroku run python manage.py migrate
## run collectstatic using bower
$  heroku run 'bower install --config.interactive=false;grunt prep;python manage.py collectstatic --noinput'
## enable collecstatic for future deploys
$  heroku config:unset DISABLE_COLLECTSTATIC
## try it on your own (optional)
$  heroku run python manage.py collectstatic
```