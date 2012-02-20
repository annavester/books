from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from books_app.authors.models import Author
#from books_app.authors.forms import AuthorSaveForm, AddWebsiteForm, AddBioForm, AddWikiForm
from books_app.readinglists.models import ReadingList 

def authors_listing(request, extra_context=None, template_name='books/authors/listing.html'):
    authors_list  = Author.objects.all()
        
    vars = RequestContext(request, {'authors':authors_list})
    return render_to_response(template_name, vars)

def view_author(request, author_id, extra_context=None, template_name='author.html'):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    reading_lists = ReadingList.objects.all()    
    
    if request.method == 'POST':   
        a = Author.objects.get(id=int(author.id))  
        if request.POST.get('website'):  
            form = AddWebsiteForm(request.POST)
            if form.is_valid():                 
                a.website = form.cleaned_data['website']
                a.save()      
        if request.POST.get('bio'):
            form = AddBioForm(request.POST)
            if form.is_valid():
                a.bio = form.cleaned_data['bio']
                a.save()
        if request.POST.get('wiki'):
            form = AddWikiForm(request.POST)
            if form.is_valid():
                a.wiki = form.cleaned_data['wiki']
                a.save()
                
    vars = RequestContext(request, {'author':author, 'books':books, 'reading_list':reading_lists})
    return render_to_response(template_name, vars)

@login_required
def save_author(request, extra_content=None, template_name='books/authors/add_author.html'):
    if request.method == 'POST':
        form = AuthorSaveForm(request.POST)
        if form.is_valid():               
            form.save()   
    else:
        form = AuthorSaveForm()
    vars = RequestContext(request, {'save_form': form})
    return render_to_response(template_name, vars)

@login_required
def add_website(request, author_id, template_name='books/add_website.html'):    
    author = get_object_or_404(Author, id=author_id)
    form = AddWebsiteForm()  
    vars = RequestContext(request, {'author':author, 'form':form })       
    return render_to_response(template_name, vars)

@login_required
def add_bio(request, author_id, template_name='books/add_bio.html'):    
    author = get_object_or_404(Author, id=author_id)
    form = AddBioForm()  
    vars = RequestContext(request, {'author':author, 'form':form })       
    return render_to_response(template_name, vars)

@login_required
def add_wiki(request, author_id, template_name='books/add_wiki.html'):    
    author = get_object_or_404(Author, id=author_id)
    form = AddWikiForm()  
    vars = RequestContext(request, {'author':author, 'form':form })       
    return render_to_response(template_name, vars)