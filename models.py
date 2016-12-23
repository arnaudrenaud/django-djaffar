from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class BrowsingActivity(models.Model):
    user = models.ForeignKey(User, null=True)
    session = models.ForeignKey(Session, null=True)
    ip_address = models.CharField(max_length=45, default='')
    date_time = models.DateTimeField()
    path = models.CharField(max_length=1000)
    referrer = models.CharField(max_length=160, default='')

    def __str__(self):
        try:
            user = self.user.username
        except (ObjectDoesNotExist, AttributeError,):
            user = 'ANONYMOUS'
        try:
            session = self.session.pk
        except (ObjectDoesNotExist, AttributeError,):
            session = 'NOSESSION'
        return '{0}, {1}, {2}, {3}, {4}, {5}'.format(
            user, session, self.ip_address,
            self.date_time, self.path, self.referrer)


class SessionInfo(models.Model):
    session = models.OneToOneField(
        Session,
        primary_key=True)
    user_agent = models.CharField(max_length=1000)
