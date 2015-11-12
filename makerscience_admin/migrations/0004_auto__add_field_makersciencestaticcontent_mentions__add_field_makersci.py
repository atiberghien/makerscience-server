# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MakerScienceStaticContent.mentions'
        db.add_column(u'makerscience_admin_makersciencestaticcontent', 'mentions',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MakerScienceStaticContent.facebook'
        db.add_column(u'makerscience_admin_makersciencestaticcontent', 'facebook',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MakerScienceStaticContent.twitter'
        db.add_column(u'makerscience_admin_makersciencestaticcontent', 'twitter',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MakerScienceStaticContent.linkedin'
        db.add_column(u'makerscience_admin_makersciencestaticcontent', 'linkedin',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MakerScienceStaticContent.youtube'
        db.add_column(u'makerscience_admin_makersciencestaticcontent', 'youtube',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MakerScienceStaticContent.mentions'
        db.delete_column(u'makerscience_admin_makersciencestaticcontent', 'mentions')

        # Deleting field 'MakerScienceStaticContent.facebook'
        db.delete_column(u'makerscience_admin_makersciencestaticcontent', 'facebook')

        # Deleting field 'MakerScienceStaticContent.twitter'
        db.delete_column(u'makerscience_admin_makersciencestaticcontent', 'twitter')

        # Deleting field 'MakerScienceStaticContent.linkedin'
        db.delete_column(u'makerscience_admin_makersciencestaticcontent', 'linkedin')

        # Deleting field 'MakerScienceStaticContent.youtube'
        db.delete_column(u'makerscience_admin_makersciencestaticcontent', 'youtube')


    models = {
        u'makerscience_admin.makersciencestaticcontent': {
            'Meta': {'object_name': 'MakerScienceStaticContent'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_cgu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_faq': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_team': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkedin': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mentions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'project_thematic_selection': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'project_selection'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['taggit.Tag']"}),
            'resource_thematic_selection': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'resource_selection'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['taggit.Tag']"}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'youtube': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'makerscience_admin.pageviews': {
            'Meta': {'object_name': 'PageViews'},
            'client': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['makerscience_admin']