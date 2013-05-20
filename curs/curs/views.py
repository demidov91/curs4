from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import Http404, HttpResponse
from utils import CustomValidationError

from registration.utils import get_profile
from registration.models import Userprofile
from utils import TextareaParser, FileEmailParser

import logging
logger = logging.getLogger(__name__)


data_parsers = {
    'text': TextareaParser,
    'file': FileEmailParser,
}


@login_required
def contacts(request):
    me = get_profile(request.user)     
    template_name = 'client_contacts.html' if me.is_client else 'user_contacts.html'   
    errors = False
    text_emails = ''
    if request.POST:
        data_type = request.POST['data_type']
        text_emails = request.POST.get('emails', '')
        data_parser = data_parsers[data_type](request)
        try:
            data_parser.save()    
        except CustomValidationError as e:
            errors = e        
        else:
            return redirect('contacts')
    return render(request, template_name, {
        'contacts': me.knows.all(),
        'errors': errors,
        'text_emails': text_emails,
        })
        
def delete_contact(request):
    username = request.POST['username']
    to_disconnect = Userprofile.index.get(username=request.POST['username'])
    get_profile(request.user).knows.disconnect(to_disconnect)
    return HttpResponse('')
