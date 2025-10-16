from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from urllib.parse import urlparse
from pathlib import PurePosixPath

import requests
from requests.utils import requote_uri

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Быстрое добавление данных на сайт при помощи ссылки на .json файл.'

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            type=str,
            help='Ссылка на .json файл с данными.'
        )

    def handle(self, *args, **options):
        url = requote_uri(options['url'])

        response = requests.get(url)
        response.raise_for_status()

        place_data = response.json()

        place, created = Place.objects.get_or_create(
            title=place_data['title'],
            latitude=place_data['coordinates']['lat'],
            longitude=place_data['coordinates']['lng'],
            defaults={
                'short_description': place_data['description_short'],
                'long_description': place_data['description_long'],
            }
        )

        if created:
            for image_url in place_data['imgs']:
                response = requests.get(image_url)
                response.raise_for_status()

                parsed_url = urlparse(image_url)
                image_name = PurePosixPath(parsed_url.path).name

                image_obj = Image(
                    place=place
                )
                image_obj.image.save(
                    image_name, ContentFile(response.content), save=False
                )
                image_obj.save()

        else:
            print('Данное место уже есть в базе данных.')






# https://raw.githubusercontent.com/devmanorg/where-to-go-places/refs/heads/master/places/Японский%20сад.json