from django.db import models


class Podcast(models.Model):
    title = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    feed = models.URLField()
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def title_or_unnamed(self):
        return self.title if self.title else 'unnamed'


class Episode(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    podcast = models.ForeignKey(Podcast)
    published = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title
