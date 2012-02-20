from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from books_app.readinglists.models import ReadingList
#from books_app.readinglists.forms import ReadingListSaveForm

def reading_list_listing(request, extra_context=None, template_name='books/reading_lists/listing.html'):
    reading_lists = ReadingList.objects.all()
    reading_lists_paged = Paginator(reading_lists, 25)
    
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        reading_lists_list = reading_lists_paged.page(page)
    except (EmptyPage, InvalidPage):
        reading_lists_list = reading_lists_paged.page(reading_lists_paged.num_pages)
        
    vars = RequestContext(request, {'reading_lists_list':reading_lists_list})
    return render_to_response(template_name, vars)

def view_reading_list(request, reading_list_id, extra_context=None, template_name='reading_list.html'):
    reading_list = get_object_or_404(ReadingList, id=reading_list_id)    
    books = reading_list.books.all().order_by('-lastupdated')
    finished_books = books.filter(status=1).count()
    reading_now = books.filter(status=3).count()
    havenotread = books.filter(status=2).count()
    vars = RequestContext(request, {'reading_list':reading_list, 'finished_books':finished_books, 'reading_now':reading_now, 'havenotread':havenotread, 'books':books})
    return render_to_response(template_name, vars)

@login_required
def save_reading_list(request, extra_content=None, template_name='books/authors/add_readinglist.html'):
    if request.method == 'POST':
        form = ReadingListSaveForm(request.POST)
        if form.is_valid():               
            form.save()   
    else:
        form = ReadingListSaveForm()
    vars = RequestContext(request, {'save_form': form})
    return render_to_response(template_name, vars)