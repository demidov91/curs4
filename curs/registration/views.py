from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.contrib.auth.forms import UserCreationForm

from utils import check_client
from userpart.utils import get_advertisment_to_show



def login(request):
    if not request.user.is_authenticated():
        return auth_views.login(request,  template_name='login.html')
    if check_client(request.user):
        return redirect('client_index')
    campaign = get_advertisment_to_show(request)
    if not campaign:
        raise Http404()
    return redirect('show_adv', campaign_id=campaign.id)

def logout(request):
    django_logout(request)
    return redirect('index')


def register(request):
    form = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=request.POST['password1'])
            django_login(request, user)
            return redirect('index')
    form = form or UserCreationForm()
    return render(request, 'register.html', {'form': form})   
     
        