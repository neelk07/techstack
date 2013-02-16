from django.conf.urls import patterns, include, url
from techstack_app.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'techstack.views.home', name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin', include(admin.site.urls)),
    url(r'^companies', companies_page),
    # url(r'^companies/new', add_company_page),
    url(r'^new', add_company_page),
    url(r'^company/(\d+)$', company_page),
    url(r'', home_page),
)


