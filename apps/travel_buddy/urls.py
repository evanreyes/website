from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^/register$', views.register, name="register"),
    url(r'^/login$', views.login, name="login"),
    url(r'^/logout$', views.logout, name="logout"),
    url(r'^/travels$', views.travels, name="travels"),
    url(r'^/travels/add$', views.addtrip, name="addtrip"),
    url(r'^/travels/createtrip$', views.createtrip, name="createtrip"),
    url(r'^/travels/destination/(?P<id>\d+)$', views.destination, name="destination"),
    url(r'^/travels/join/(?P<id>\d+)$', views.join, name='join'),
]
