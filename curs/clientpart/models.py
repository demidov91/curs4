from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
import os

from curs.utils import graph_db
from py2neo.neo4j import WriteBatch, Node
from py2neo.rest import ResourceNotFound

import logging
logger = logging.getLogger(__name__)



class ActiveCampaignManager(models.Manager):
    '''
    Manager Campaign filter by Active status
    '''
    def get_query_set(self):
        return super(ActiveCampaignManager, self).get_query_set() \
                .filter( startdate__lte=datetime.date.today(), finishdate__gte=datetime.date.today() )
       


class Campaign(models.Model):
    title = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    client = models.ForeignKey(User, related_name="campaigns")    
    startdate = models.DateField('Campaign Start Date', default=datetime.date.today, db_index=True)
    finishdate = models.DateField('Campaign Finish Date', db_index=True)
    picture = models.ImageField(upload_to='uploads/campaign_images', max_length=255, null=True, blank=True)
    salary = models.PositiveIntegerField(default=0)
    gift = models.PositiveIntegerField(default=0)
    was_launched = models.BooleanField(default=False)
    
    nodes_index_name = 'clientpart_campaign'
    contact_relationship = 'CONTACT'
    
    graph_db.get_or_create_index(Node, nodes_index_name)
    
    objects = models.Manager()
    actives = ActiveCampaignManager()
    
    def get_node(self):
        index = graph_db.get_index(Node, self.nodes_index_name)
        return index.get('id', str(self.id))[0]
        
        
        
    def set_contacts(self, profiles):
        """
        *profiles* -- registration.models.Userprofile objects.
        """
        me = self.get_node()
        batch = WriteBatch(graph_db)
        for profile in profiles:
            batch.get_or_create_relationship(me, self.contact_relationship, profile.__node__)
        r = batch.submit()
        logger.warn(r)
        
    def get_contacts(self):
        """
        Returns a list of related usernames (str). 
        """
        logger.warn(tuple(profile_node['username'] for profile_node in self.get_node().get_related_nodes(0, self.contact_relationship)))
        return tuple(profile_node['username'] for profile_node in self.get_node().get_related_nodes(0, self.contact_relationship))
        
    
    def save(self, *args, **kwargs):
        logger.warn('Save camp')
        is_new = False
        if not self.id:
            is_new = True
        super(Campaign, self).save(*args, **kwargs)
        if is_new:
            index = graph_db.get_index(Node, self.nodes_index_name)
            node = index.create('id', str(self.id), {'campaign_id': self.id})  
            logger.warn(node)   
            
    def delete(self, *args, **kwargs):
        batch = WriteBatch(graph_db)
        node = self.get_node()
        for rel in node.get_relationships():
            batch.delete_relatioship(rel)
        batch.delete_node(node)
        super(Campaign, self).delete(*args, **kwargs)
    

