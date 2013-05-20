from openpyxl import Workbook
from StringIO import StringIO


from django.shortcuts import render, redirect
import django
from django.db import transaction
from django.http import HttpResponse

from forms import CampaignForm
from models import Campaign
from registration.utils import get_profile, clients_only, campaign_owners_only

import logging
logger = logging.getLogger(__name__)

@clients_only
def index(request):
    campaigns = Campaign.objects.filter(client=request.user)
    return render(request, 'all_campaigns.html', {'campaigns': campaigns})

@clients_only
@transaction.commit_manually
def create_campaign(request):
    if request.method == 'POST':
        campaign = Campaign(client=request.user)
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            campaign = form.save()
            if campaign.id:
                return redirect('client_index')
    if request.method == 'GET':
        form = CampaignForm()
    form.fields['contacts'].widget = django.forms.widgets.CheckboxSelectMultiple(choices=((c.username, c.username) for c in get_profile(request.user).knows.all())) 
    transaction.commit()
    return render(request, 'new_campaign.html', {
            'form': form,
        })
        
@campaign_owners_only(set_key='campaign')        
def get_contacts_for_campaign(request, campaign):
    return render(request, 'campaign_contacts_list.html', {'contacts': campaign.get_contacts(), 'campaign': campaign})

@campaign_owners_only(set_key='campaign')  
def export_campaign(request, campaign):
    wb = Workbook(optimized_write = True)
    ws = wb.create_sheet()
    for contact in campaign.get_contacts():
        logger.warn(contact)
        ws.append([contact])
    out = StringIO()
    wb.save(out)
    response = HttpResponse(out.getvalue(), content_type='application/vnd.ms-excel')
    return response
    
   
    