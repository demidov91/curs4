from django.db import models
from django.conf import settings
import datetime
import os



class ActiveCampaignManager(models.Manager):
    '''
    Manager Campaign filter by Active status
    '''
    def get_query_set(self):
        return super(ActiveCampaignManager, self).get_query_set() \
                .filter( startdate__lte=datetime.date.today(), finishdate__gte=datetime.date.today() )
       


class Campaign(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="campaigns")
    actives = ActiveCampaignManager()
    startdate = models.DateField('Campaign Start Date', default=datetime.date.today, db_index=True)
    finishdate = models.DateField('Campaign Start Date', db_index=True)
    picture = models.ImageField(upload_to=os.path.join(settings.PUBLIC_UPLOAD_DIR, 'capaign_images'), null=True)
    salary = models.PositiveIntegerField(default=0)
    gift = models.PositiveIntegerField(default=0)
    start_date = models.DateField(default=datetime.date(year=2000, month=1, day=1))
    finish_date = models.DateField(default=datetime.date(year=2000, month=1, day=1))
    was_launched = models.BooleanField(default=False)
    

