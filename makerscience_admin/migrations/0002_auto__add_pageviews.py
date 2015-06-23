# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageViews'
        db.create_table(u'makerscience_admin_pageviews', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('resource_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'makerscience_admin', ['PageViews'])


    def backwards(self, orm):
        # Deleting model 'PageViews'
        db.delete_table(u'makerscience_admin_pageviews')


    models = {
        u'makerscience_admin.makersciencestaticcontent': {
            'Meta': {'object_name': 'MakerScienceStaticContent'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_cgu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_faq': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_team': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'makerscience_admin.pageviews': {
            'Meta': {'object_name': 'PageViews'},
            'client': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['makerscience_admin']