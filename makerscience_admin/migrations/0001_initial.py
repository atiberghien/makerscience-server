# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MakerScienceStaticContent'
        db.create_table(u'makerscience_admin_makersciencestaticcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('about', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('about_team', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('about_contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('about_faq', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('about_cgu', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'makerscience_admin', ['MakerScienceStaticContent'])


    def backwards(self, orm):
        # Deleting model 'MakerScienceStaticContent'
        db.delete_table(u'makerscience_admin_makersciencestaticcontent')


    models = {
        u'makerscience_admin.makersciencestaticcontent': {
            'Meta': {'object_name': 'MakerScienceStaticContent'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_cgu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_faq': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_team': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['makerscience_admin']