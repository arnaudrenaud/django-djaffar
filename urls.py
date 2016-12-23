from django.conf.urls import url

from browsingactivity import views

urlpatterns = [
    url(r'^$', views.BrowsingActivities.as_view()),
]
