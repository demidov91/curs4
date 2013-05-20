import neomodel

from registration.models import Userprofile
import logging
from neomodel.exception import DoesNotExist
from py2neo.neo4j import WriteBatch

logger = logging.getLogger(__name__)

def check_client(user):
    profile = get_profile(user)
    return profile.is_client if profile else False

def get_profile(user):
    try:
        return Userprofile.index.get(username=user.username)
    except DoesNotExist:
        return None

           
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

