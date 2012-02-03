from django.conf.urls.defaults import patterns, include, url

from views import index, about, contact

import settings

urlpatterns = patterns('red.views',
    url(r'^$',       index),
    url(r'^about',   about),
    url(r'^contact', contact),
)

if settings.DEBUG:
    from os import path
    red_dir = path.normpath(path.dirname(__file__))
    static_dir = path.join(red_dir, 'static')
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static_dir}),
    )
