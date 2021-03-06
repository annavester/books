import os
from django.conf import settings
from django.conf.urls import patterns, include, url, handler404, handler500
from django.views.generic import TemplateView
from books.views import book_listing, book_stats, book_charts, view_book, update_status, update_own,save_book, delete_book,get_latest_read,get_reading_now,add_to_list
from authors.views import view_author, authors, add_website, add_bio, add_wiki, save_author
from readinglists.views import view_reading_list
from accounts.views import logout_page
site_media = os.path.join(settings.PROJECT_DIR, 'static')

urlpatterns = patterns('',
    url(r'^$', book_listing, name='books'),
    url(r'^(?P<status_id>[1-3]+)/$', book_listing, name='books_by_status'),
    url(r'^stats/$', book_stats, name='view_stats'),
    url(r'^stats/(?P<year>[0-9]{4})/$', book_stats, name='view_stats_by_year'),
    url(r'^chart-data/$', book_charts),
    url(r'^api/v1/latest_read/(?P<count>[0-9]{0,4})/$', get_latest_read),
    url(r'^api/v1/reading_now/(?P<count>[0-9]{0,4})/$', get_reading_now),
    url(r'^book/(?P<book_id>[0-9]+)/$', view_book, name='view_book'),
    url(r'^book/(?P<book_id>[0-9]+)/update_status$', update_status, name='update_status'),
    url(r'^book/(?P<book_id>[0-9]+)/update_own$', update_own, name='update_own'),
    url(r'^book/(?P<book_id>[0-9]+)/add_to_list$', add_to_list, name='add_to_list'),
    url(r'^book/(?P<book_id>[0-9]+)/delete$', delete_book, name='delete_book'),
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
    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt")),
    url(r'^google43980db1e9ad016a.html$', TemplateView.as_view(template_name="google43980db1e9ad016a.html")),
)
