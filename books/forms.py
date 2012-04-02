from django import forms
from django.forms import ModelMultipleChoiceField
from django.utils.safestring import mark_safe
from books_app.authors.models import Author
from models import Book, Binding, Category, Status
from books_app.readinglists.models import ReadingList

class AuthorModelChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        if not obj.last_name and not obj.first_name:
            return "%s"%(obj.company_name)
        else:
            # Return a string of the format: "lastname, firstname"
            return "%s, %s"%(obj.last_name, obj.first_name)
 
class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


RATING_CHOICES = (
                  ('0', '--'),
                  ('1', '1'),
                  ('2', '2'),
                  ('3', '3'),
                  ('4', '4'),
                  ('5', '5'),
                  ('6', '6'),
                  ('7', '7'),
                  ('8', '8'),
                  ('9', '9'),
)

OWN_CHOICES = ( 
               ('0', 'No'),
               ('1', 'Yes')
)

class BookSaveForm(forms.ModelForm):
    title = forms.CharField(label=u'Book Title')
    authors = AuthorModelChoiceField(queryset=Author.objects.all().order_by('last_name'),widget=forms.SelectMultiple(attrs={"size":5}))
    isbn = forms.CharField(label=u'ISBN')
    binding = forms.ModelChoiceField(queryset=Binding.objects.all().order_by('name'), empty_label='--')    
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), empty_label='--')    
    status = forms.ModelChoiceField(queryset=Status.objects.all().order_by('name'), empty_label='--')
    own = forms.CharField(label="Do you own this book?", widget=forms.RadioSelect(renderer=HorizRadioRenderer, choices=(('1','Yes'),('0','No'))), required=True)
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    amazon_link = forms.CharField(label=u'Amazon/Google Link')
    imagepath = forms.FileField(label=u'Image Path')
    pages = forms.IntegerField()
    editorial = forms.CharField(widget=forms.Textarea)
    review = forms.CharField(widget=forms.Textarea, required=False)
    readinglist =forms.ModelChoiceField(queryset=ReadingList.objects.all().order_by('name'), empty_label='--', required=False)
    datefinished = forms.DateField(required=False)
    
    class Meta:
        model = Book
        exclude = ('filename',)

class SearchBooksForm(forms.Form):
    query = forms.CharField(label=u'Enter a keyword to search for',widget=forms.TextInput(attrs={'size':32}))
    
class BookUpdateStatusForm(forms.Form):
    status = forms.ModelChoiceField(label='Status',queryset=Status.objects.all().order_by('name'), empty_label='--')
    rating = forms.ChoiceField(label='Rating',choices=RATING_CHOICES)
    review = forms.CharField(label='Review',required=False)
    datefinished = forms.DateField(label='Date Finished',required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        book_status = self.cleaned_data['status']
        rating = cleaned_data.get('rating')
        review = cleaned_data.get('review')
        datefinished = cleaned_data.get('datefinished')
        
        if book_status.name == 'Already Read':
            if not review:
                raise forms.ValidationError("Please write a brief review.")            
            if not datefinished:
                raise forms.ValidationError("Please select date finished.")
            if not rating:                
                raise forms.ValidationError("Please choose rating.")
        return cleaned_data
    
class BookAddToListForm(forms.Form):
    readinglist=forms.ModelChoiceField(label='Reading List',queryset=ReadingList.objects.all().order_by('name'), empty_label='--')
    
class BookUpdateOwnForm(forms.Form):
    own = forms.ChoiceField(choices=OWN_CHOICES)
