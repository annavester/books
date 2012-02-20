from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db import models
from models import Book,Category
#from books.forms import BookSaveForm, SearchBooksForm, BookUpdateStatusForm, BookAddToListForm
#from authors.models import Author
#from readinglists.models import ReadingList
import os
#from pyaws import ecs
#import settings
from endless_pagination.decorators import page_template

@page_template('listing_page.html')
def book_listing(request, extra_context=None, template='home.html'):
    context = {
        'read_books':Book.objects.select_related().filter(status=1).count(),        
        'havenotread_books':Book.objects.select_related().filter(status=2).count(),
        'readingnow_books':Book.objects.select_related().filter(status=3).count(),
        'books': Book.objects.select_related().all().order_by('-lastupdated'),
    }
    
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))

#def user_page(request, username):
    #try:
        #user = User.objects.get(username = username)
    #except User.DoesNotExist:
    #    raise Http404(u'Requested user not found.')
    
    #if request.method == 'POST':
    #    book_id = request.POST['book_id']
    #    author_id = request.POST['author_id']
    #    book = Book.objects.get(id=int(book_id))
    #    author = Author.objects.get(id=int(author_id))
    #    book.authors.add(author)
    
    #ecs.setLicenseKey(settings.AMZ_KEY_ID)
    #ecs.setSecretKey(settings.AMZ_SECRET)
    #ecs.setLocale('us')
    #aws_book = {}
    #isbn = '9780980104004'
    #aws_book = ecs.ItemLookup(ItemId=isbn, IdType='ISBN', SearchIndex='Books', ResponseGroup='Medium')

    #book_wout_author = []
    #cat_id = '35'
    #category_name = Category.objects.filter(id = int(cat_id)).values_list('name', flat=True)
    #books = Book.objects.filter(category = int(cat_id))#[160:180]
    #for book in books:
    #    if not book.authors.all():
    #        book_wout_author.append(book)
    #        
    #allauthors = Author.objects.all().order_by("last_name")
    #       
    #vars = RequestContext(request, {'books': book_wout_author, 'authors':allauthors, 'category_name': category_name })
    #vars = RequestContext(request, { 'book': aws_book })
    #return render_to_response('user_page.html', vars)

def view_book(request, book_id, extra_context=None, template_name='books/book.html', temp_ajax='books/book_item.html'):
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

#    form = SearchBooksForm()
#    books = []
#    show_results = False
#    if 'query' in request.GET:
#        show_results = True
#        query = request.GET.get('query').strip()
#        if query:
#            form = SearchBooksForm({'query': query})
#            books = Book.objects.filter(title__icontains=query)[:10]
    vars = RequestContext(request, {
        'form':form, 
        'book':book, 
        'reading_list':reading_lists, 
        'show_results':show_results ,
        'result':books})
    
    if request.GET.has_key('ajax'):
        return render_to_response(temp_ajax,vars)
    else:
        return render_to_response(template_name, vars)

#@login_required
#def save_book(request, template_name='books/add_book.html'):
#    if request.method == 'POST':
#        form = BookSaveForm(request.POST,request.FILES)
#        if form.is_valid():               
#            book = form.save(commit=False)          
#            book.filename = request.FILES['imagepath'].name
#            book.save()        
#            b2a = Book.objects.get(id=int(book.pk))   
#            authors = []
#            authors = form.cleaned_data['authors']
#            for author in authors:
#                author_obj = Author.objects.get(id=int(author.id))
#                b2a.authors.add(author_obj)      
#    else:
#        form = BookSaveForm()
#    vars = RequestContext(request, {'save_form': form})
#    return render_to_response(template_name, vars)

#@login_required
#def update_status(request, book_id, template_name='books/update_status.html'):    
#    book = get_object_or_404(Book, id=book_id)
#    form = BookUpdateStatusForm()  
#    vars = RequestContext(request, {'book':book, 'form':form })       
#    return render_to_response(template_name, vars)

#@login_required
#def add_to_list(request, book_id, template_name='books/add_to_list.html'):    
#    book = get_object_or_404(Book, id=book_id)
#    form = BookAddToListForm()  
#    vars = RequestContext(request, {'book':book, 'form':form })       
#    return render_to_response(template_name, vars)

#def search_books(request, temp_static='books/search.html', temp_ajax='books/book_item.html'):
#    form = SearchBooksForm()
#    books = []
#    show_results = False
#    if 'query' in request.GET:
#        show_results = True
#        query = request.GET['query'].strip()
#        if query:
#            form = SearchBooksForm({'query': query})
#            books = Book.objects.filter(title__icontains=query)[:10]
#    vars = RequestContext(request, {'form':form, 'books':books, 'show_results':show_results})
#    if request.GET.has_key('ajax'):
#        return render_to_response(temp_ajax,vars)
#    else:
#        return render_to_response(temp_static,vars)