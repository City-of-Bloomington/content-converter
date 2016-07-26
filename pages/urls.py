from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<page_id>[\w-]+)/$', views.details, name='details'),
    url(r'^(?P<page_id>[\w-]+)/comment$', views.comment, name='comment'),
]
