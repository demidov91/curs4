from neomodel.exception import DoesNotExist
from lucenequerybuilder import Q

from django import forms
from django.core.validators import email_re
from django.forms import ValidationError
from django.db import transaction

from clientpart.models import Campaign
from registration.utils import get_profile
from registration.models import Userprofile

import logging
logger = logging.getLogger(__name__)


class ContactsField(forms.MultipleChoiceField):
    def validate(self, value):
        for email in value:
            if not email_re.match(email):
                raise ValidationError('Incorrect choice.')



class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ['client', 'was_launched']
        
    def clean_contacts(self):
        me = get_profile(self.instance.client)
        profiles = []
        for contact in self.cleaned_data['contacts']:
            try:
                p = Userprofile.index.get(username=contact)
            except DoesNotExist as e:
                logger.warn(contact)
                raise ValidationError("Can't be connected to {0}".format(contact))
            if not me.knows.is_connected(p):
                raise ValidationError("Can't be connected to {0}".format(contact))
            profiles.append(p)
        return profiles
          
    contacts = ContactsField()
        
    def save(self, *args, **kwargs):
        campaign = super(CampaignForm, self).save()
        try:
            campaign.set_contacts(self.cleaned_data['contacts'])
        except Exception as e:
            logger.error(e)
            transaction.rollback()
            raise e
        else:
            transaction.commit()
        return campaign
        
    