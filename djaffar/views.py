from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from dateutil import parser
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from django.conf import settings
from django.contrib.sessions.models import Session

from .models import Activity, SessionInfo



class LogActivity(views.APIView):

    def _session(self, request):
        if not request.session.exists(request.session.session_key):
            request.session.create()
            session = Session.objects.get(pk=request.session.session_key)
            SessionInfo.objects.get_or_create(
                session=session,
                user_agent=request.META.get('HTTP_USER_AGENT', ''))
        try:
            session_id = request.session.session_key
            try:
                session = Session.objects.get(pk=session_id)
            except ObjectDoesNotExist:
                session = None
        except KeyError:
            session = None
        return session

    def post(self, request):
        user = request.user
        if user.is_anonymous():
            user = None
        session = self._session(request)
        ip_address = request.META.get('REMOTE_ADDR', '')
        dt = request.data.get('date')
        if not dt:
            return Response(
                'You must provide a date',
                status=status.HTTP_400_BAD_REQUEST)
        try:
            date = parser.parse(dt)
        except ValueError:
                return Response(
                    'You must provide a valid date',
                    status=status.HTTP_400_BAD_REQUEST)
        path = (request.data.get('path') or
                urlparse(request.META.get('HTTP_REFERER', '')).path)
        if not path:
            return Response(
                'You must provide a path',
                status=status.HTTP_400_BAD_REQUEST)
        referer = request.data.get('referer', '')
        Activity.objects.create(
            user=user,
            session=session,
            ip_address=ip_address,
            date=date,
            path=path,
            referer=referer)
        return Response(status=status.HTTP_201_CREATED)
