from rest_framework import views
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from dateutil import parser

from browsingactivity.models import BrowsingActivity, SessionInfo
from django.contrib.sessions.models import Session


class BrowsingActivities(views.APIView):
    authentication_classes = (OAuth2Authentication,)

    def post(self, request):
        request.session.set_expiry(31547000)
        if not request.session.exists(request.session.session_key):
            request.session.create()
            session = Session.objects.get(pk=request.session.session_key)
            SessionInfo.objects.get_or_create(
                session=session,
                user_agent=request.META.get('HTTP_USER_AGENT', ''))
        user = request.user
        if user.is_anonymous():
            user = None
        try:
            session_id = request.session.session_key
            try:
                session = Session.objects.get(pk=session_id)
            except ObjectDoesNotExist:
                session = None
        except KeyError:
            session = None
        path = request.data.get('path')
        if not path:
            return Response(
                'You must provide a path',
                status=status.HTTP_400_BAD_REQUEST)
        dt = request.data.get('date_time')
        if not dt:
            return Response(
                'You must provide a date',
                status=status.HTTP_400_BAD_REQUEST)
        try:
            date_time = parser.parse(dt)
        except ValueError:
                return Response(
                    'You must provide a valid date',
                    status=status.HTTP_400_BAD_REQUEST)
        referrer = request.data.get('referrer')
        if referrer == 'NOT_FIRST_PAGE' or not referrer:
            referrer = ''
        ip_address = request.META.get('REMOTE_ADDR', '')
        BrowsingActivity.objects.create(
            user=user,
            session=session,
            ip_address=ip_address,
            date_time=date_time,
            path=path,
            referrer=referrer)
        return Response(status=status.HTTP_201_CREATED)
