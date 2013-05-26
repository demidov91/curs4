from functools import wraps

import neomodel

from registration.models import Userprofile


import logging
from neomodel.exception import DoesNotExist
from py2neo.neo4j import WriteBatch
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

def check_client(user):
    profile = get_profile(user)
    return profile.is_client if profile else False

def get_profile(user):
    try:
        return Userprofile.index.get(username=user.username)
    except DoesNotExist:
        return None
    
def get_profile_node(user):
    return get_profile(user).__node__

           
def create_connections(owner, recipients):
    """
    *owner* - Userprofile.
    *recipient* - collection of Userprofile.
    """
    for recipient in recipients:
        recipient.get_set_client_lock().acquire()
        try:
            if not recipient.is_client and not recipient == owner:
                owner.knows.connect(recipient)
        except Exception as e:
            logger.error(e)
        finally:
            recipient.get_set_client_lock().release()


def clients_only(wrapped):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not check_client(request.user):
            raise PermissionDenied()
        return wrapped(request, *args, **kwargs)
    return wrapper



class campaign_owners_only:
    """
    Check for campaign_id variable in kwargs. Response-403 for clients that don't own this campaign.
    Updates *kwargs* with the fetched campaign.
    """
    def __init__(self, set_key=None, get_key='campaign_id'):
        """
        The decorated function will be launched with bongocampaign.models.Campaign as *set_key* kwarg and without
        original *get_key* kwarg (campaign_id default).
        """
        self.set_key = set_key
        self.get_key = get_key
    def __call__(self, view_func):
        from clientpart.models import Campaign
        @clients_only
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            campaign_id = kwargs.get(self.get_key)
            campaign = get_object_or_404(Campaign.objects, id=campaign_id)
            if not campaign.client == request.user:
                raise PermissionDenied()
            kwargs[self.set_key] = campaign
            del kwargs[self.get_key]
            return view_func(request, *args, **kwargs)
        return wrapper
    
    
def users_only(wrapped):
    @login_required
    def wrapper(request, *args, **kwargs):
        if check_client(request.user):
            raise PermissionDenied()
        return wrapped(request, *args, **kwargs)
    return wrapper    
    
