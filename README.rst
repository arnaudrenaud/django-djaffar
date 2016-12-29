Djaffar: asynchronous user activity tracking for Django
=======================================================

|Build Status| |PyPI version|

Want to keep track of what your users do even when they don't hit the
server? Set up Djaffar on the server and make a request to the client
API to log user activity to the database, including URI path, user name,
browser session, IP address and user agent.

Requirements
------------

Django (1.8, 1.9, 1.10).

Installation
------------

Install with ``pip``:

::

    pip install django-djaffar

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

When sending a POST request to Djaffar to log activity, you should care
about the following properties:

+----------------+------------+-------+---------+----------+--------+
| Property name  | Mandatory  | Type  | Format  | Example  | Usage  |
+================+============+=======+=========+==========+========+
| ``date``       | Yes        | Form  | ISO     | ``2016-1 | Repres |
|                |            | data  | 8601    | 2-29T07: | ents   |
|                |            |       |         | 35:22.57 | the    |
|                |            |       |         | 1Z``     | date   |
|                |            |       |         |          | and    |
|                |            |       |         |          | time   |
|                |            |       |         |          | when   |
|                |            |       |         |          | the    |
|                |            |       |         |          | log    |
|                |            |       |         |          | reques |
|                |            |       |         |          | t      |
|                |            |       |         |          | is     |
|                |            |       |         |          | initia |
|                |            |       |         |          | ted.   |
+----------------+------------+-------+---------+----------+--------+
| ``path``       | No         | Form  | -       | ``users/ | Repres |
|                |            | data  |         | me/cart/ | ents   |
|                |            |       |         | ``       | the    |
|                |            |       |         |          | path   |
|                |            |       |         |          | taken  |
|                |            |       |         |          | by the |
|                |            |       |         |          | user.  |
|                |            |       |         |          | If not |
|                |            |       |         |          | specif |
|                |            |       |         |          | ied,   |
|                |            |       |         |          | the    |
|                |            |       |         |          | refere |
|                |            |       |         |          | r      |
|                |            |       |         |          | *from  |
|                |            |       |         |          | the    |
|                |            |       |         |          | reques |
|                |            |       |         |          | t      |
|                |            |       |         |          | header |
|                |            |       |         |          | s*     |
|                |            |       |         |          | (not   |
|                |            |       |         |          | the    |
|                |            |       |         |          | ``refe |
|                |            |       |         |          | rer``  |
|                |            |       |         |          | form   |
|                |            |       |         |          | data   |
|                |            |       |         |          | proper |
|                |            |       |         |          | ty)    |
|                |            |       |         |          | will   |
|                |            |       |         |          | be     |
|                |            |       |         |          | used   |
|                |            |       |         |          | in     |
|                |            |       |         |          | place. |
+----------------+------------+-------+---------+----------+--------+
| ``referer``    | No         | Form  | -       | ``https: | Repres |
|                |            | data  |         | //www.go | ents   |
|                |            |       |         | ogle.com | the    |
|                |            |       |         | /``      | domain |
|                |            |       |         |          | the    |
|                |            |       |         |          | user   |
|                |            |       |         |          | comes  |
|                |            |       |         |          | from.  |
+----------------+------------+-------+---------+----------+--------+

Examples
~~~~~~~~

Basic log
^^^^^^^^^

Request Djaffar to log an activity with the current date:

.. code:: javascript

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/djaffar/logs/', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send('date=' + new Date().toISOString());

URL fragments
^^^^^^^^^^^^^

If your client app relies on URL fragments for navigation, you'll need
to manually set the ``path`` parameter when you hit Djaffar:

.. code:: javascript

    ...
    xhr.send(... + '&path=' + (window.location.href.split('#')[1] || '/'))

User authentication
^^^^^^^^^^^^^^^^^^^

-  If you use session-based authentication, the cookie is automatically
   set in the request headers by your browser.
-  But if you use token-based authentication, you'll need to set the
   token in the request headers, like so:

   .. code:: javascript

       ...
       xhr.setRequestHeader('Authorization', 'Bearer F2naN20HpDv4tsJC0b1OhQZVDwRiEy');
       xhr.send(...)

Retrieving activity logs
------------------------

Logs are stored as instances of the ``Activity`` model (in
``djaffar.models``) and have the following properties:

+-------------------+--------------+-------------------+
| Model field name  | Description  | Model field type  |
+===================+==============+===================+
| ``user``          | Instance of  | ``ForeignKey``    |
|                   | the ``User`` |                   |
|                   | model if     |                   |
|                   | authenticate |                   |
|                   | d,           |                   |
|                   | ``None``     |                   |
|                   | otherwise    |                   |
+-------------------+--------------+-------------------+
| ``session``       | User browser | ``ForeignKey``    |
|                   | session,     |                   |
|                   | instance of  |                   |
|                   | the          |                   |
|                   | ``Session``  |                   |
|                   | model        |                   |
+-------------------+--------------+-------------------+
| ``ip_address``    | User         | ``CharField``     |
+-------------------+--------------+-------------------+
| ``date``          | User         | ``DateTimeField`` |
|                   | activity     |                   |
|                   | date and     |                   |
|                   | time         |                   |
+-------------------+--------------+-------------------+
| ``path``          | User         | ``CharField``     |
|                   | activity     |                   |
|                   | path         |                   |
+-------------------+--------------+-------------------+
| ``referer``       | User         | ``CharField``     |
|                   | activity     |                   |
|                   | referer      |                   |
+-------------------+--------------+-------------------+

.. figure:: https://trello-attachments.s3.amazonaws.com/5841a8e7863eaf470b1e5d57/585d6cb3d8336749a4162b7f/c6717d6623b04b3f791718c88e9f21a1/Screen_Shot_2016-12-27_at_10.15.08.png
   :alt: Accessing logs from the Django shell

   Accessing logs from the Django shell

Djaffar also adds the ``SessionInfo`` model, linked to the ``Session``
model through a foreign key, with the following properties:

+--------------------+-------------------------------------+--------------------+
| Model field name   | Description                         | Model field type   |
+====================+=====================================+====================+
| ``user_agent``     | User agent of the browser session   | ``CharField``      |
+--------------------+-------------------------------------+--------------------+

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

.. |Build Status| image:: https://travis-ci.org/arnaudrenaud/django-djaffar.svg?branch=master
   :target: https://travis-ci.org/arnaudrenaud/django-djaffar
.. |PyPI version| image:: https://badge.fury.io/py/django-djaffar.svg
   :target: https://badge.fury.io/py/django-djaffar
