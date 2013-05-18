from registration.models import Userprofile
import logging

def check_client(user):
    profile = Userprofile.index.search(user_id=user.id)
    return profile and not profile.is_client

