from django.db import models
from authors.models import Author
from readinglists.models import ReadingList
from settings import UPLOAD_DIR

class Book(models.Model):    
    authors = models.ManyToManyField(Author, related_name='books')
    title = models.CharField(max_length=450)
    isbn = models.CharField(max_length=25)
    binding = models.ForeignKey('Binding')
    category = models.ForeignKey('Category')
    status = models.ForeignKey('Status')
    own = models.BooleanField()
    rating = models.IntegerField(null=True, blank=True)
    amazon_link = models.CharField(max_length=6000, blank=True)
    imagepath = models.FileField(upload_to=UPLOAD_DIR)
    filename =models.CharField(max_length=200, null=True)
    pages = models.IntegerField(null=True, blank=True)
    editorial = models.CharField(max_length=6000, blank=True)
    review = models.CharField(max_length=2000, blank=True)
    readinglist = models.ManyToManyField(ReadingList, related_name='books')
    datefinished = models.DateField(null=True, blank=True)
    lastupdated = models.DateTimeField(auto_now=True)
    dateadded = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title
    
class Binding(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)    
    
    def __unicode__(self):
        return self.name
    
class Status(models.Model):
    name = models.CharField(max_length=15)
    
    def __unicode__(self):
        return self.name   