from django.conf.urls import patterns, url, include
from django.conf import settings
from views import *
from curs.views import contacts

urlpatterns = patterns('',
    url(r'^$', index, name="client_index"),
    url(r'^campaign/create/$', create_campaign, name="create_new_campaign"),
    url(r'^campaign/export/(?P<campaign_id>\d+)/$', export_campaign, name="export_campaign"),
    url(r'^contacts/$', contacts, {'template_name': 'client_contacts.html'}, name="client_contacts"),
    url(r'^ajax/campaign/contacts/(?P<campaign_id>\d+)/$', get_contacts_for_campaign, name='ajax_get_campaign_contacts'),
)
