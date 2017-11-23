from django.conf.urls import url
from . import views 
          
urlpatterns = [
    url(r'^main$', views.loginregpage),  
    url(r'^login$', views.login),
    url(r'^registration$', views.registration),
    url(r'^dashboard$', views.renderdash),
    url(r'^wish_items/create$', views.additemrender),
    url(r'^(?P<userid>\d+)/additem$', views.additem),
    url(r'^(?P<itemid>\d+)/addtowishlist$', views.addtowishlist),
    url(r'^wish_items/(?P<itemid>\d+)', views.itemdisplay),
    url(r'^(?P<itemid>\d+)/remove$', views.remove),
    url(r'^(?P<itemid>\d+)/delete$', views.delete),
    url(r'^logout$', views.logout)
]