# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MakerSciencePost'
        db.create_table(u'makerscience_forum_makersciencepost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['megafon.Post'])),
            ('post_type', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'makerscience_forum', ['MakerSciencePost'])


    def backwards(self, orm):
        # Deleting model 'MakerSciencePost'
        db.delete_table(u'makerscience_forum_makersciencepost')


    models = {
        u'makerscience_forum.makersciencepost': {
            'Meta': {'object_name': 'MakerSciencePost'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['megafon.Post']"}),
            'post_type': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'megafon.post': {
            'Meta': {'object_name': 'Post'},
            'answers_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'answers'", 'null': 'True', 'to': u"orm['megafon.Post']"}),
            'posted_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "('id',)", 'max_length': '50', 'populate_from': 'None'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['makerscience_forum']