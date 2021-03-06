from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from settings import STATIC_URL
from app.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^main/$', main, name='main'),
    url(r'^todo/?$', todo, name='todo'),
    url(r'^add_friend/?$', add_friend, name='add_friend'),
    url(r'^delete_friend/(?P<friend>[0-9]+)/?$', delete_friend, name='delete_friend'),
    url(r'^update_task/(?P<id>[0-9]+)/$', update_task, name='update_task'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^accounts/(.*)$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_URL}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
