from django.conf.urls import url

from .views import LogActivity

urlpatterns = [
    url(r'^logs/$', LogActivity.as_view()),
]
