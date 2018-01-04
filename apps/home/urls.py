from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^about_me$', views.about),
    url(r'^projects$', views.projects),
    url(r'^blog$', views.blog)
]
