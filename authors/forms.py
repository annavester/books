from django import forms
from django.utils.safestring import mark_safe
from models import Author

class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class AuthorSaveForm(forms.ModelForm):
    first_name = forms.CharField(label=u'First Name')
    last_name = forms.CharField(label=u'Last Name')    
    company_name = forms.CharField(label=u'Company Name',required=False)
    bio = forms.CharField(label=u'Bio', widget=forms.Textarea, required=False)
    wiki = forms.CharField(required=False)
    favorite = forms.CharField(label="Is this your favorite Author?", widget=forms.RadioSelect(renderer=HorizRadioRenderer, choices=(('1','Yes'),('0','No'))), required=True)
    website = forms.CharField(label=u'Author\'s website',required=False)
    
    class Meta:
        model = Author
        
class AddWebsiteForm(forms.Form):
    website = forms.CharField(label="Author's Website",required=False)   
    
class AddBioForm(forms.Form):
    bio = forms.CharField(label="Author's Bio",required=False, widget=forms.Textarea(attrs={'cols':20,'rows':5}))
    
class AddWikiForm(forms.Form):
    wiki = forms.CharField(label="Author's Wiki",required=False)