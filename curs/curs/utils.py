import datetime

import neomodel
from py2neo import neo4j
from openpyxl import load_workbook

from django.contrib.auth.models import User
from django.core.validators import email_re
from django.forms import ValidationError
from django.conf import settings

from registration.utils import get_profile, create_connections
from registration.models import Userprofile
from  registration.utils import check_client
from define import DATETIME_FORMAT
import logging
logger = logging.getLogger(__name__)


class CustomValidationError(Exception):
    pass 



class AbstractContactsParser(object):
    emails = ()
    
    def __init__(self, request):
        self.profile = get_profile(request.user)

    def validate(self):
        for email in self.emails:
            if not email_re.match(email):
                raise CustomValidationError('{0} is not a propper email.'.format(email))
        users = User.objects.filter(username__in=self.emails)
        for user in users:
            if check_client(user):
                raise CustomValidationError("You can't connect to {0}".format(user.username))
        
    def save(self):
        self.validate()
        logger.warn(self.emails)
        recipients = []
        for username in self.emails:
            recipients.append(Userprofile.get_or_create(username=username))
        logger.warn(recipients)
        create_connections(self.profile, recipients)
        
        

class TextareaParser(AbstractContactsParser):
    def __init__(self, request):
        super(TextareaParser, self).__init__(request)
        self.emails = request.POST['emails'].split()
        
        
class FileEmailParser(AbstractContactsParser):
    def __init__(self, request):
        super(FileEmailParser, self).__init__(request)
        workbook = load_workbook(request.FILES['emails'])
        self.emails = tuple(row[0].value for row in workbook.get_active_sheet().rows)
        logger.warn(self.emails)
        
graph_db = neo4j.GraphDatabaseService(settings.NEO4J_REST_URL)


def messages_context_processor(request):
    return get_profile(reuqest.user).pull_messages()

def datetime_serialize(date_time):
    return datetime.datetime.strftime(date_time, DATETIME_FORMAT)

def datetime_deserialize(date_time):
    return datetime.datetime.strptime(date_time, DATETIME_FORMAT)
            
   
            
            