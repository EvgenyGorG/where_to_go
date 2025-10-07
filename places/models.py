from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

