from django.conf.urls import patterns, url, include
from django.conf import settings
from views import *
from curs.views import contacts

urlpatterns = patterns('',
    url(r'^(?P<campaign_id>\d+)/$', show_adv, name="show_adv"),
)
