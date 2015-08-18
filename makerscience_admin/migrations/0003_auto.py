# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field project_thematic_selection on 'MakerScienceStaticContent'
        m2m_table_name = db.shorten_name(u'makerscience_admin_makersciencestaticcontent_project_thematic_selection')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('makersciencestaticcontent', models.ForeignKey(orm[u'makerscience_admin.makersciencestaticcontent'], null=False)),
            ('tag', models.ForeignKey(orm[u'taggit.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['makersciencestaticcontent_id', 'tag_id'])

        # Adding M2M table for field resource_thematic_selection on 'MakerScienceStaticContent'
        m2m_table_name = db.shorten_name(u'makerscience_admin_makersciencestaticcontent_resource_thematic_selection')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('makersciencestaticcontent', models.ForeignKey(orm[u'makerscience_admin.makersciencestaticcontent'], null=False)),
            ('tag', models.ForeignKey(orm[u'taggit.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['makersciencestaticcontent_id', 'tag_id'])


    def backwards(self, orm):
        # Removing M2M table for field project_thematic_selection on 'MakerScienceStaticContent'
        db.delete_table(db.shorten_name(u'makerscience_admin_makersciencestaticcontent_project_thematic_selection'))

        # Removing M2M table for field resource_thematic_selection on 'MakerScienceStaticContent'
        db.delete_table(db.shorten_name(u'makerscience_admin_makersciencestaticcontent_resource_thematic_selection'))


    models = {
        u'makerscience_admin.makersciencestaticcontent': {
            'Meta': {'object_name': 'MakerScienceStaticContent'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_cgu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_faq': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'about_team': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_thematic_selection': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'project_selection'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['taggit.Tag']"}),
            'resource_thematic_selection': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'resource_selection'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['taggit.Tag']"})
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