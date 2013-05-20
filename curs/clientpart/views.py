from django.shortcuts import render, redirect
import django
from django.db import transaction

from forms import CampaignForm
from models import Campaign
from registration.utils import get_profile

import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'all_campaigns.html', {})

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
    return render(request, 'new_campaign.html', {
            'form': form,
        })
    