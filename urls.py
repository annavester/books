import os
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url, handler404, handler500
from django.views.generic.simple import direct_to_template
from main.views import mainpage
#from account.views import register_page, logout_page
site_media = os.path.join(settings.PROJECT_DIR, 'static')

urlpatterns = patterns('',
    url(r'^$', mainpage),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^logout/$', logout_page),
    #url(r'^register/$', register_page),
    #url(r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),    
    #url(r'^books/', include('books.urls')),    
)

urlpatterns += patterns('django.views.generic.simple',
    #url(r'^robots.txt$', 'direct_to_template', {'template':'robots.txt', 'mimetype':'text/plain'}),
    #url(r'^google43980db1e9ad016a.html$', 'direct_to_template', {'template':'google43980db1e9ad016a.html', 'mimetype':'text/plain'}),
    #url(r'^dancer.html$', 'direct_to_template', {'template':'dancer.html', 'mimetype':'text/html'}),
)