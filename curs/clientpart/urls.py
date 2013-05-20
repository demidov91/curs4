from django.conf.urls import patterns, url, include
from django.conf import settings
from views import *
from curs.views import contacts

urlpatterns = patterns('',
    url(r'^$', index, name="client_index"),
    url(r'^campaign/create/$', index, name="create_new_campaign"),
    url(r'^contacts/$', contacts, {'template_name': 'client_contacts.html'}, name="client_contacts"),
)
