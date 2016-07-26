from django.conf.urls import url

from . import views

app_name = 'topics'
urlpatterns = [
    url(r'^(?P<topic_tag>[\w-]+)/$', views.details, name='details'),
    url(r'^$', views.index, name='index'),
    
]
