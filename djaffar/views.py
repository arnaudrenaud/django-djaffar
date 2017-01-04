from rest_framework import views, serializers, status
from rest_framework.response import Response
from django.conf import settings
from django.contrib.sessions.models import Session

from .models import Activity, SessionInfo


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class SessionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionInfo
        fields = '__all__'


def get_user_pk(user):
    if user.is_anonymous():
        return None
    return user.pk

def get_path(path, referer):
    if not path:
        return referer
    return path


class ActivityDetail(views.APIView):

    def _set_new_session(self, request):
        request.session.create()
        return request.session.session_key

    def _get_session(self, request):
        if not request.session.exists(request.session.session_key):
            return self._set_new_session(request)
        return request.session.session_key

    def _save_activity(self, request):
        serializer = ActivitySerializer(data={
            'user': get_user_pk(request.user),
            'session': self._get_session(request),
            'ip_address': request.META.get('REMOTE_ADDR', ''),
            'date': request.data.get('date', ''),
            'path': get_path(
                request.data.get('path', ''),
                request.META.get('HTTP_REFERER', ''),
            ),
            'referer': request.data.get('referer', ''),
        })
        if not serializer.is_valid():
            return {'errors': serializer.errors}
        serializer.save()
        return serializer.instance

    def _save_session_info_if_new(self, request):
        session_key = Session.objects.get(pk=request.session.session_key)
        try:
            session_info = SessionInfo.objects.get(session=session_key)
        except SessionInfo.DoesNotExist:
            session_info = SessionInfo.objects.create(
                session=session_key,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
        return session_info

    def post(self, request):
        activity = self._save_activity(request)
        if isinstance(activity, dict) and 'errors' in activity:
            return Response(
                activity,
                status=status.HTTP_400_BAD_REQUEST,
            )
        self._save_session_info_if_new(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
