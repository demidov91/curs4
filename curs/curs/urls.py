
from django.conf import settings
from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^auth/', include('registration.urls')),
    (r'^advert/', include('userpart.urls')),
    (r'^manage/', include('clientpart.urls')),
    url(r'^$', 'registration.views.login', name="index"),
)


