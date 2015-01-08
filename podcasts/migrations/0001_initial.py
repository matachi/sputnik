# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('parent_category', models.ForeignKey(to='podcasts.Category', null=True, blank=True, related_name='child_category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField(blank=True, max_length=500)),
                ('description', models.TextField(blank=True)),
                ('published', models.DateTimeField(blank=True)),
                ('audio_file', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('link', models.URLField(blank=True)),
                ('feed', models.URLField()),
                ('metadata_feed', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='podcasts')),
                ('language', models.CharField(blank=True, max_length=2)),
                ('title_lock', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('categories', models.ManyToManyField(to='podcasts.Category', blank=True, related_name='podcasts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PodcastUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('listened_to', models.ManyToManyField(to='podcasts.Episode', blank=True, related_name='listeners')),
                ('subscribed_to', models.ManyToManyField(to='podcasts.Podcast', blank=True, related_name='subscribers')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='podcasts_profile')),
            ],
            options={
                'verbose_name': "User's Podcasts profile",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='podcast',
            name='tags',
            field=models.ManyToManyField(to='podcasts.Tag', blank=True, related_name='podcasts'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='episode',
            name='podcast',
            field=models.ForeignKey(to='podcasts.Podcast', related_name='episodes'),
            preserve_default=True,
        ),
    ]
