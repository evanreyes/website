from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^/books$', views.books, name="books"),
    url(r'^/books/add$', views.newbook, name="newbook"),
    url(r'^/books/create$', views.createbook, name="createbook"),
    url(r'^/books/(?P<id>\d+)$', views.bookinfo, name="bookinfo"),
    url(r'^/users/(?P<id>\d+)$', views.userprofile, name="userprofile"),
    url(r'^/newreview/(?P<id>\d+)$', views.newreview, name="newreview"),
    url(r'^/deletereview/(?P<id>\d+)$', views.deletereview, name="deletereview")
]
