from threading import Lock

import neomodel
from neomodel import StructuredNode, StringProperty, RelationshipTo,\
 BooleanProperty, IntegerProperty, RelationshipFrom
from py2neo.neo4j import WriteBatch, Node, Direction
from neomodel.exception import DoesNotExist

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.core.validators import email_re
from django.forms import ValidationError
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

import logging
logger = logging.getLogger(__name__)


for field in User._meta.local_fields:
    if field.name == 'username':
        User._meta.local_fields.remove(field)
        break

User.add_to_class('username', models.EmailField('email', unique=True))


    
class Userprofile(StructuredNode):
    is_client = BooleanProperty(default=False)
    username = StringProperty(index=True)
    knows = RelationshipTo('Userprofile', 'KNOWS')
    known = RelationshipFrom('Userprofile', 'KNOWS')
    
    _create_locks = {}
    _set_client_locks = {}
    
    def set_is_client(self, is_client):
        if not is_client:
            self.is_client = False
            self.save()
            return
        batch = WriteBatch(neomodel.core.connection())
        for rel in self.known.all():
            batch.delete(rel)
        batch.set_node_property(self.__node__, 'is_client', True)
        self.get_set_client_lock().acquire()
        try:
            batch.submit()
        finally:
            self.get_set_client_lock().release()
    
    @classmethod    
    def get_create_lock(cls, username):
        return cls._create_locks.setdefault(username, Lock())  
    
    def get_set_client_lock(self):
        return self._set_client_locks.setdefault(self, Lock())  
    
    @classmethod
    def get_or_create(cls, **keyvalue):
        """
        To be modified and moved to neomodel.Index.
        """
        category_node = cls.category().__node__
        node = cls.index.__index__.get_or_create('username', keyvalue['username'], keyvalue)
        if not category_node.is_related_to(node, Direction.OUTGOING, cls.relationship_type()):
            category_node.create_relationship_to(node, cls.relationship_type(), {'__instance__': True})
        structured = cls()
        structured.__node__ = node
        structured.refresh()
        return structured 
    
    
    
        
def after_user_save(instance, created, **kwargs):
    username = getattr(instance, 'username')
    if username:
        if not email_re.match(username):
            raise ValidationError('Username must be an email.')
    if created:
        Userprofile.get_or_create(username=instance.username)


post_save.connect(after_user_save, sender=User)