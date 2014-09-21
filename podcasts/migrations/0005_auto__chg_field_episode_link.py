# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Episode.link'
        db.alter_column('podcasts_episode', 'link', self.gf('django.db.models.fields.URLField')(max_length=500))

    def backwards(self, orm):

        # Changing field 'Episode.link'
        db.alter_column('podcasts_episode', 'link', self.gf('django.db.models.fields.URLField')(max_length=300))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'podcasts.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['podcasts.Category']", 'blank': 'True', 'null': 'True', 'related_name': "'child_category'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'podcasts.episode': {
            'Meta': {'object_name': 'Episode'},
            'audio_file': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '500'}),
            'podcast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['podcasts.Podcast']", 'related_name': "'episodes'"}),
            'published': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'podcasts.podcast': {
            'Meta': {'object_name': 'Podcast'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['podcasts.Category']", 'blank': 'True', 'related_name': "'podcasts'", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feed': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'language': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '2'}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'metadata_feed': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['podcasts.Tag']", 'blank': 'True', 'related_name': "'podcasts'", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'title_lock': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'podcasts.podcastuserprofile': {
            'Meta': {'object_name': 'PodcastUserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listened_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['podcasts.Episode']", 'blank': 'True', 'related_name': "'listeners'", 'symmetrical': 'False'}),
            'subscribed_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['podcasts.Podcast']", 'blank': 'True', 'related_name': "'subscribers'", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'related_name': "'podcasts_profile'"})
        },
        'podcasts.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['podcasts']