from django.conf.urls import url

from . import views

app_name = 'departments'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<department_tag>[\w-]+)/$', views.pages, name='pages'),
]
