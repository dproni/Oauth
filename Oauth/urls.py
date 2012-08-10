from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from settings import STATIC_URL
from app.views import *
from app.facebook import facebook_view
from app.odnoklassniki import ok_app, ok_app_info

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^form2/$', form2, name='form2'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^ok/$', ok_app , name='ok_app'),
    url(r'^ok/info/$', ok_app_info , name='ok_app_info'),
    url(r'', include('social_auth.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_URL}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
