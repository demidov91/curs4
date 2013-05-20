from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout

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
    return redirect('show_adv', camapign_id=campaign.id)

def logout(request):
    django_logout(request)
    return redirect('index')


    
        