# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Campaign.picture'
        db.add_column(u'clientpart_campaign', 'picture',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'Campaign.salary'
        db.add_column(u'clientpart_campaign', 'salary',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Campaign.gift'
        db.add_column(u'clientpart_campaign', 'gift',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Campaign.start_date'
        db.add_column(u'clientpart_campaign', 'start_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2000, 1, 1, 0, 0)),
                      keep_default=False)

        # Adding field 'Campaign.finish_date'
        db.add_column(u'clientpart_campaign', 'finish_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2000, 1, 1, 0, 0)),
                      keep_default=False)

        # Adding field 'Campaign.was_launched'
        db.add_column(u'clientpart_campaign', 'was_launched',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Campaign.picture'
        db.delete_column(u'clientpart_campaign', 'picture')

        # Deleting field 'Campaign.salary'
        db.delete_column(u'clientpart_campaign', 'salary')

        # Deleting field 'Campaign.gift'
        db.delete_column(u'clientpart_campaign', 'gift')

        # Deleting field 'Campaign.start_date'
        db.delete_column(u'clientpart_campaign', 'start_date')

        # Deleting field 'Campaign.finish_date'
        db.delete_column(u'clientpart_campaign', 'finish_date')

        # Deleting field 'Campaign.was_launched'
        db.delete_column(u'clientpart_campaign', 'was_launched')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'clientpart.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaigns'", 'to': u"orm['auth.User']"}),
            'finish_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'finishdate': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'gift': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'salary': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'startdate': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'db_index': 'True'}),
            'was_launched': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['clientpart']