from django.shortcuts import render_to_response
from django.template import RequestContext
#from books.models import Book
import urllib2
from django.utils import simplejson

def mainpage(request, extra_context=None, template_name='home.html'):    
    #reading_books = Book.objects.select_related().filter(status=3).order_by("-lastupdated")[:5]
    #finished_books = Book.objects.select_related().filter(status=1).order_by("-lastupdated")[:5]
    
    url = "http://api.twitter.com/1/statuses/user_timeline.json?screen_name=annavester&count=5"
    response = urllib2.urlopen(urllib2.Request(url))
    tweets = simplejson.load(response)

           
    vars = RequestContext(request, {
        #'reading_books':reading_books, 
        #'finished_books':finished_books, 
        'tweets':tweets})
    return render_to_response(template_name, vars)