from django.conf.urls import url

from .views import ActivityDetail

urlpatterns = [
    url(r'^logs/$', ActivityDetail.as_view(), name='activity_detail'),
]
