from django.db import models
from django.db.models import PositiveSmallIntegerField


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name='заголовок')
    short_description = models.TextField(blank=True, verbose_name='краткое описание')
    long_description = models.TextField(blank=True, verbose_name='расширенное описание')
    latitude = models.FloatField(blank=True, null=True, verbose_name='широта')
    longitude = models.FloatField(blank=True, null=True, verbose_name='долгота')

    def __str__(self):
        return self.title


class Image(models.Model):
    order = PositiveSmallIntegerField(verbose_name='номер изображения')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images', verbose_name='место')
    image = models.ImageField(upload_to='places/images/', verbose_name='изображение')

    def __str__(self):
        return f'{self.order} - {self.place.title}'