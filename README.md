# Djaffar: asynchronous user activity tracking for Django
[![Build Status](https://travis-ci.org/arnaudrenaud/django-djaffar.svg?branch=master)](https://travis-ci.org/arnaudrenaud/django-djaffar)
[![PyPI version](https://badge.fury.io/py/django-djaffar.svg)](https://badge.fury.io/py/django-djaffar)

Want to keep track of what your users do even when they don't hit the server? Set up Djaffar on the server and POST a request to the client API to log user activity to the database, including URL path, user name, browser session, user agent, and IP address.


## Installation

Add Djaffar to your project (typically in `settings.py`):
```python
INSTALLED_APPS = [
    ...
    'djaffar',
]
```

Specify the URL that will be used to hit Djaffar (typically in `urls.py`):
```python
from django.conf.urls import url, include

urlpatterns = [
    ...
    url(r'^djaffar/', include('djaffar.urls')),
]
```

Make sure the authentication classes you use for your users are specified in the Django Rest Framework settings (typically in `settings.py`):
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'path.to.AuthenticationClass',
    )
}
```

Run the database migration:
```
$ python manage.py migrate djaffar
```

## Client API

POST an activity log to Djaffar with the current date:
```javascript
var xhr = new XMLHttpRequest();
xhr.open('POST', '/djaffar/logs/', true);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send('date=' + new Date().toISOString());
```

You can then trigger this POST request everytime the URL changes, for instance.

### Path and URL fragments
If your client app relies on URL fragments for navigation, you'll need to manually set the `path` parameter when you hit Djaffar:
```javascript
...
xhr.send(... + '&path=' + (window.location.href.split('#')[1] || '/'))
```

### User authentication

- If you use session-based authentication, the cookie is automatically set in the request headers by your browser.
- But if you use token-based authentication, you'll need to set the token in the request headers, like so:
```
...
xhr.setRequestHeader('Authorization', 'Bearer F2naN20HpDv4tsJC0b1OhQZVDwRiEy');
xhr.send(...)
```

## Retrieving activity logs

Logs are stored as instances of the `Activity` model:

![Accessing logs from the Django shell](https://trello-attachments.s3.amazonaws.com/5841a8e7863eaf470b1e5d57/585d6cb3d8336749a4162b7f/c6717d6623b04b3f791718c88e9f21a1/Screen_Shot_2016-12-27_at_10.15.08.png)

## Appendix

### About sessions
Djaffar uses [Django sessions](https://docs.djangoproject.com/en/1.10/topics/http/sessions/) to keep track of browser sessions when logging user activity. Depending on settings, sessions either expire when the user closes their browser or after a given age (see [Browser-length sessions vs. persistent sessions](https://docs.djangoproject.com/en/1.10/topics/http/sessions/#browser-length-vs-persistent-sessions)).

Whether your app uses session-based user authentication or not, Djaffar uses session (and the associated user agent) for two reasons:

- Allowing you to distinguish between anonymous visitors
- Allowing you to distinguish between visits by the same authenticated user through various devices

## Tests

Run tests (`tests/tests.py`) against the supported versions of Python and the required packages, as listed in `tox.ini`:
```
tox
```