from django.conf.urls import patterns, url, include
from django.conf import settings
from views import *


urlpatterns = patterns('',
    url(r'^$', index, name="client_index"),
)
