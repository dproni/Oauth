from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from settings import STATIC_URL
from app.views import *
import app

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^main/$', main, name='main'),
#    url(r'^add/(?P<task_id>\d{1,4})/$', app.views.addTask, name='addTask'),
#    url(r'^delete/(?P<task_id>\d{1,4})/$', deleteTask, name='deleteTask'),
#    url(r'^share/(?P<task_id>\d{1,4})/$', shareBoard, name='shareBoard'),
    url(r'^add/$', app.views.addTask, name='addTask'),
    url(r'^delete/$', deleteTask, name='deleteTask'),
    url(r'^share/$', shareBoard, name='shareBoard'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_URL}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
