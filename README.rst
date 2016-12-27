Djaffar: asynchronous user activity tracking for Django
=======================================================

Want to keep track of what your users do even when they don't hit the
server? Set up Djaffar on the server and POST a request to the client
API to log user activity to the database, including URL path, user name,
browser session, user agent, and IP address.

Installation
------------

Add Djaffar to your project (typically in ``settings.py``):

.. code:: python

    INSTALLED_APPS = [
        ...
        'djaffar',
    ]

Specify the URL that will be used to hit Djaffar (typically in
``urls.py``):

.. code:: python

    from django.conf.urls import url, include

    urlpatterns = [
        ...
        url(r'^djaffar/', include('djaffar.urls')),
    ]

Make sure the authentication classes you use for your users are
specified in the Django Rest Framework settings (typically in
``settings.py``):

.. code:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            ...
            'path.to.AuthenticationClass',
        )
    }

Run the database migration:

::

    $ python manage.py migrate djaffar

Client API
----------

POST an activity log to Djaffar with the current date:

.. code:: javascript

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/djaffar/track/', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send('date=' + new Date().toISOString());

You can then trigger this POST request everytime the URL changes, for
instance.

Path and URL fragments
~~~~~~~~~~~~~~~~~~~~~~

If your client app relies on URL fragments for navigation, you'll need
to manually set the ``path`` parameter when you hit Djaffar:

.. code:: javascript

    ...
    xhr.send(... + '&path=' + (window.location.href.split('#')[1] || '/'))

User authentication
~~~~~~~~~~~~~~~~~~~

-  If you use session-based authentication, the cookie is automatically
   set in the request headers by your browser.
-  But if you use token-based authentication, you'll need to set the
   token in the request headers, like so:

   ::

       ...
       xhr.setRequestHeader('Authorization', 'Bearer F2naN20HpDv4tsJC0b1OhQZVDwRiEy');
       xhr.send(...)

Retrieving activity logs
------------------------

Appendix
--------

About sessions
~~~~~~~~~~~~~~

Djaffar uses `Django
sessions <https://docs.djangoproject.com/en/1.10/topics/http/sessions/>`__
to keep track of browser sessions when logging user activity. Depending
on settings, sessions either expire when the user closes their browser
or after a given age (see `Browser-length sessions vs. persistent
sessions <https://docs.djangoproject.com/en/1.10/topics/http/sessions/#browser-length-vs-persistent-sessions>`__).

Whether your app uses session-based user authentication or not, Djaffar
uses session (and the associated user agent) for two reasons:

-  Allowing you to distinguish between anonymous visitors
-  Allowing you to distinguish between visits by the same authenticated
   user through various devices

Tests
-----

Run tests (``tests/tests.py``) against the supported versions of Python
and the required packages, as listed in ``tox.ini``:

::

    tox
