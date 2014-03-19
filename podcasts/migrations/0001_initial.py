# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('podcasts_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('podcasts', ['Tag'])

        # Adding model 'Category'
        db.create_table('podcasts_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['podcasts.Category'], related_name='child_category')),
        ))
        db.send_create_signal('podcasts', ['Category'])

        # Adding model 'Podcast'
        db.create_table('podcasts_podcast', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('link', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200)),
            ('feed', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('metadata_feed', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(blank=True, max_length=100)),
            ('language', self.gf('django.db.models.fields.CharField')(blank=True, max_length=2)),
            ('title_lock', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(blank=True, max_length=50)),
        ))
        db.send_create_signal('podcasts', ['Podcast'])

        # Adding M2M table for field tags on 'Podcast'
        m2m_table_name = db.shorten_name('podcasts_podcast_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('podcast', models.ForeignKey(orm['podcasts.podcast'], null=False)),
            ('tag', models.ForeignKey(orm['podcasts.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['podcast_id', 'tag_id'])

        # Adding M2M table for field categories on 'Podcast'
        m2m_table_name = db.shorten_name('podcasts_podcast_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('podcast', models.ForeignKey(orm['podcasts.podcast'], null=False)),
            ('category', models.ForeignKey(orm['podcasts.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['podcast_id', 'category_id'])

        # Adding model 'Episode'
        db.create_table('podcasts_episode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('link', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('podcast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['podcasts.Podcast'], related_name='episodes')),
            ('published', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('audio_file', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200)),
        ))
        db.send_create_signal('podcasts', ['Episode'])

        # Adding model 'PodcastUserProfile'
        db.create_table('podcasts_podcastuserprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, related_name='podcasts_profile')),
        ))
        db.send_create_signal('podcasts', ['PodcastUserProfile'])

        # Adding M2M table for field subscribed_to on 'PodcastUserProfile'
        m2m_table_name = db.shorten_name('podcasts_podcastuserprofile_subscribed_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('podcastuserprofile', models.ForeignKey(orm['podcasts.podcastuserprofile'], null=False)),
            ('podcast', models.ForeignKey(orm['podcasts.podcast'], null=False))
        ))
        db.create_unique(m2m_table_name, ['podcastuserprofile_id', 'podcast_id'])

        # Adding M2M table for field listened_to on 'PodcastUserProfile'
        m2m_table_name = db.shorten_name('podcasts_podcastuserprofile_listened_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('podcastuserprofile', models.ForeignKey(orm['podcasts.podcastuserprofile'], null=False)),
            ('episode', models.ForeignKey(orm['podcasts.episode'], null=False))
        ))
        db.create_unique(m2m_table_name, ['podcastuserprofile_id', 'episode_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('podcasts_tag')

        # Deleting model 'Category'
        db.delete_table('podcasts_category')

        # Deleting model 'Podcast'
        db.delete_table('podcasts_podcast')

        # Removing M2M table for field tags on 'Podcast'
        db.delete_table(db.shorten_name('podcasts_podcast_tags'))

        # Removing M2M table for field categories on 'Podcast'
        db.delete_table(db.shorten_name('podcasts_podcast_categories'))

        # Deleting model 'Episode'
        db.delete_table('podcasts_episode')

        # Deleting model 'PodcastUserProfile'
        db.delete_table('podcasts_podcastuserprofile')

        # Removing M2M table for field subscribed_to on 'PodcastUserProfile'
        db.delete_table(db.shorten_name('podcasts_podcastuserprofile_subscribed_to'))

        # Removing M2M table for field listened_to on 'PodcastUserProfile'
        db.delete_table(db.shorten_name('podcasts_podcastuserprofile_listened_to'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'podcasts.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['podcasts.Category']", 'related_name': "'child_category'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'podcasts.episode': {
            'Meta': {'object_name': 'Episode'},
            'audio_file': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'podcast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['podcasts.Podcast']", 'related_name': "'episodes'"}),
            'published': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'podcasts.podcast': {
            'Meta': {'object_name': 'Podcast'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['podcasts.Category']", 'related_name': "'podcasts'"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feed': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'language': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '2'}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'metadata_feed': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['podcasts.Tag']", 'related_name': "'podcasts'"}),
            'title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'title_lock': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'podcasts.podcastuserprofile': {
            'Meta': {'object_name': 'PodcastUserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listened_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['podcasts.Episode']", 'related_name': "'listeners'"}),
            'subscribed_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['podcasts.Podcast']", 'related_name': "'subscribers'"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'related_name': "'podcasts_profile'"})
        },
        'podcasts.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['podcasts']