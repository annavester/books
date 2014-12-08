from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db import models
from models import Book,Category
from forms import BookSaveForm, SearchBooksForm, BookUpdateStatusForm, BookUpdateOwnForm, BookAddToListForm
from books_app.authors.models import Author
from books_app.readinglists.models import ReadingList
from django.db.models import Count
import os
import json
#from pyaws import ecs
#import settings
from endless_pagination.decorators import page_template

@page_template('books_listing.html')
def book_listing(request, status_id=None, extra_context=None, template='home.html'):
    if status_id is not None:
        context = {
            'books': Book.objects.select_related().filter(status=status_id),
        }
    else:
        context = {
            'listing':True,       
            'read_books':Book.objects.select_related().filter(status=1).count(),        
            'havenotread_books':Book.objects.select_related().filter(status=2).count(),
            'readingnow_books':Book.objects.select_related().filter(status=3).count(),
            'books': Book.objects.select_related().all().order_by('-lastupdated'),
        }
    
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))

def convertDateToString(o):
    DATE_FORMAT = "%Y"
    return o.strftime(DATE_FORMAT)

def book_stats(request, year=None, extra_context=None, template='stats.html'):
    context = {}
    if year is not None:
        context = {
            'year': year,
            'book_count': Book.objects.filter(datefinished__year=year).count(),
        }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))

def book_charts(request):
    years = Book.objects.dates('datefinished','year')
    chart_data = []
    record = {}

    for y in years:
        if y is not None:
            year_string = convertDateToString(y)
            book_count = Book.objects.filter(datefinished__year=year_string).count()
            chart_data.append(dict(year=year_string, count=book_count))

    return HttpResponse(json.JSONEncoder().encode(list(chart_data)), mimetype="application/json")

def view_book(request, book_id, extra_context=None, template_name='book.html'):
    book = get_object_or_404(Book, id=book_id)
    reading_lists = ReadingList.objects.all()

    if request.method == 'POST':   
        b = Book.objects.get(id=int(book.id))  
        if request.POST.get('status'):  
            form = BookUpdateStatusForm(request.POST)
            if form.is_valid():                 
                b.status = form.cleaned_data['status']
                if b.status.name == 'Already Read':
                    b.rating = form.cleaned_data['rating']
                    b.review = form.cleaned_data['review']
                    b.datefinished = form.cleaned_data['datefinished']
                b.save()      
        if request.POST.get('readinglist'):
            form = BookAddToListForm(request.POST)
            if form.is_valid():
                rl_id = form.cleaned_data['readinglist'].id
                rl = ReadingList.objects.get(id=int(rl_id))
                b.readinglist.add(rl)
        if request.POST.get('own'):
            form = BookUpdateOwnForm(request.POST)
            if form.is_valid():
                own = form.cleaned_data['own']
                if  own == '0':
                    b.own = False
                else:
                    b.own = True
                b.save()

    vars = RequestContext(request, {
        'book': book,
        'reading_list': reading_lists,
        'title': book.title })

    return render_to_response(template_name, vars)

def get_latest_read(request, count):
    books = Book.objects.select_related().filter(status=1).values('id','filename').order_by("-datefinished")[:count]    
    return HttpResponse(json.JSONEncoder().encode(list(books)), mimetype="application/json")

def get_reading_now(request, count):
    books = Book.objects.select_related().filter(status=3).values('id','filename').order_by("-lastupdated")[:count]    
    return HttpResponse(json.JSONEncoder().encode(list(books)), mimetype="application/json")
    
@login_required
def save_book(request, template_name='books/add_book.html'):
    if request.method == 'POST':
        form = BookSaveForm(request.POST,request.FILES)
        if form.is_valid():               
            book = form.save(commit=False)          
            book.filename = request.FILES['imagepath'].name
            book.save()        
            b2a = Book.objects.get(id=int(book.pk))   
            authors = []
            authors = form.cleaned_data['authors']
            for author in authors:
                author_obj = Author.objects.get(id=int(author.id))
                b2a.authors.add(author_obj)      
    else:
        form = BookSaveForm()
    vars = RequestContext(request, {'save_form': form})
    return render_to_response(template_name, vars)

@login_required
def delete_book(request, book_id):
    b = Book.objects.get(id=int(book_id))
    b.delete()
    data = {}
    data['id'] = book_id;
    return HttpResponse(json.dumps(data), content_type = "application/json")
          
@login_required
def update_status(request, book_id, template_name='books/update_status.html'):    
    book = get_object_or_404(Book, id=book_id)
    form = BookUpdateStatusForm()  
    vars = RequestContext(request, {'book':book, 'form':form })       
    return render_to_response(template_name, vars)

@login_required
def update_own(request, book_id, template_name='books/update_own.html'):    
    book = get_object_or_404(Book, id=book_id)
    form = BookUpdateOwnForm()  
    vars = RequestContext(request, {'book':book, 'form':form })       
    return render_to_response(template_name, vars)

@login_required
def add_to_list(request, book_id, template_name='books/add_to_list.html'):    
    book = get_object_or_404(Book, id=book_id)
    form = BookAddToListForm()  
    vars = RequestContext(request, {'book':book, 'form':form })       
    return render_to_response(template_name, vars)

def search_books(request, temp_static='books/search.html', temp_ajax='books/book_item.html'):
    form = SearchBooksForm()
    books = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchBooksForm({'query': query})
            books = Book.objects.filter(title__icontains=query)[:10]
    vars = RequestContext(request, {'form':form, 'books':books, 'show_results':show_results})
    if request.GET.has_key('ajax'):
        return render_to_response(temp_ajax,vars)
    else:
        return render_to_response(temp_static,vars)
