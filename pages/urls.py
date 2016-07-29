from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    #url(r'^(?P<page_id>[\w-]+)/comment/$', views.comment, name='comment'),
    url(r'^(?P<page_id>[0-9]+)/comment/$', views.comment, name='comment'),
    url(r'^(?P<page_id>[0-9]+)/comment$', views.comment),

    url(r'^(?P<page_id>\d+)/destination/(?P<destination_id>\d+)/delete/$', views.destination_delete, name='dest_delete'),
    url(r'^(?P<page_id>[0-9]+)/destination/(?P<destination_id>[0-9]+)/delete$', views.destination_delete),
    url(r'^(?P<page_id>\d+)/destination/(?P<destination_id>\d+)/$', views.destination, name='destination'),
    url(r'^(?P<page_id>[0-9]+)/destination/(?P<destination_id>[0-9]+)$', views.destination),    
    url(r'^(?P<page_id>[0-9]+)/destination/$', views.destination, name='destination'),
    url(r'^(?P<page_id>[0-9]+)/destination$', views.destination),

    url(r'^(?P<page_id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<page_id>[0-9]+)/edit$', views.edit),
    url(r'^(?P<page_id>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<page_id>[0-9]+)/delete$', views.delete),
    url(r'^(?P<page_id>[0-9]+)/$', views.details, name='details'),
    url(r'^(?P<page_id>[0-9]+)$', views.details),
    url(r'new/$', views.edit, name='new'),
    url(r'new$', views.edit),
    url(r'^$', views.index, name='index'),
]
