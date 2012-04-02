from accounts.forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
        
    vars = RequestContext(request, {'form':form})
    
    return render_to_response('registration/register.html', vars)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')       
        