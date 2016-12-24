# Djaffar: asynchronous user activity tracking for Django
Have a single-page app? Want to keep track of what your users do even when they don't hit the server? Set up Djaffar on the server and hit the client API to save relevant user activity to the database: URL path, user name, browser session, user agent, IP address and referer.

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
python manage.py migrate djaffar
```

## Client API usage

This will ask Djaffar to write a record with the current date and URL path:
```javascript
var xhr = new XMLHttpRequest();
xhr.open('POST', '/djaffar/track/', true);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send('date=' + new Date().toISOString() + '&path=' + window.location.pathname);
```

### Authentication

- If you use session-based authentication, the cookie is automatically set in the request headers by your browser.
- But if you use token-based authentication, you'll need to set the token in the request headers, like so:
```
...
xhr.setRequestHeader('Authorization', 'Bearer F2naN20HpDv4tsJC0b1OhQZVDwRiEy');
xhr.send(...)
```

### Path
You'll need to set the current user path in the `path` parameter when you hit Djaffar:

- If your client app uses URL fragments (#) for navigation:
```javascript
...
xhr.send(... + '&path=' + (window.location.href.split('#')[1] || '/'))
```
- Or if your client app uses actual distinct URLs:
```javascript
...
xhr.send(... + '&path=' + window.location.pathname)
```

## Accessing recorded activity

## Appendix

### About sessions
Djaffar uses [Django sessions](https://docs.djangoproject.com/en/1.10/topics/http/sessions/) to keep track of browser sessions when recording user activity. Depending on settings, sessions either expire when the user closes their browser or after a given age (see [Browser-length sessions vs. persistent sessions](https://docs.djangoproject.com/en/1.10/topics/http/sessions/#browser-length-vs-persistent-sessions)).

Whether your app uses session-based user authentication or not, Djaffar uses session (and the associated user agent) for two reasons:

- Allowing you to distinguish between anonymous visitors
- Allowing you to distinguish between visits by the same authenticated user through various devices