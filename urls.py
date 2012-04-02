import os
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url, handler404, handler500
from django.views.generic.simple import direct_to_template
from books.views import book_listing, view_book, update_status, update_own,save_book
from authors.views import view_author, authors, add_website, add_bio, add_wiki, save_author
from readinglists.views import view_reading_list
from accounts.views import logout_page
site_media = os.path.join(settings.PROJECT_DIR, 'static')

urlpatterns = patterns('',
    url(r'^$', book_listing, name='books'),
    url(r'^(?P<status_id>[1-3]+)/$', book_listing, name='books_by_status'),
    url(r'^book/(?P<book_id>[0-9]+)/$', view_book, name='view_book'),
    url(r'^book/(?P<book_id>[0-9]+)/update_status$', update_status, name='update_status'),
    url(r'^book/(?P<book_id>[0-9]+)/update_own$', update_own, name='update_own'),
    url(r'^book/add/$', save_book, name='add_book'),
    url(r'^authors/$', authors, name='authors'),
    url(r'^author/(?P<author_id>[0-9]+)/$', view_author, name='view_author'),
    url(r'^author/(?P<author_id>[0-9]+)/add_website$', add_website, name='add_website'),
    url(r'^auhtor/(?P<author_id>[0-9]+)/add_bio$', add_bio, name='add_bio'),  
    url(r'^author/(?P<author_id>[0-9]+)/add_wiki$', add_wiki, name='add_wiki'),  
    url(r'^author/add/$', save_author, name='add_author'),
    url(r'^rl/(?P<reading_list_id>[0-9]+)/$', view_reading_list, name='view_reading_list'),  
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^robots.txt$', 'direct_to_template', {'template':'robots.txt', 'mimetype':'text/plain'}),
    url(r'^google43980db1e9ad016a.html$', 'direct_to_template', {'template':'google43980db1e9ad016a.html', 'mimetype':'text/plain'}),
)