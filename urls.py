import os
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url, handler404, handler500
from django.views.generic.simple import direct_to_template
from books.views import book_listing
#from account.views import register_page, logout_page
site_media = os.path.join(settings.PROJECT_DIR, 'static')

urlpatterns = patterns('',
    url(r'^$', book_listing, name='books'),
    url(r'^/(?P<book_id>[0-9]+)/$', view_book, name='view_book'),
    url(r'^/(?P<author_id>[0-9]+)/$', view_author, name='view_author'),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^logout/$', logout_page),
    #url(r'^register/$', register_page),
    #url(r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^robots.txt$', 'direct_to_template', {'template':'robots.txt', 'mimetype':'text/plain'}),
    url(r'^google43980db1e9ad016a.html$', 'direct_to_template', {'template':'google43980db1e9ad016a.html', 'mimetype':'text/plain'}),
)