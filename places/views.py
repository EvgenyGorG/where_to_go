from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def index(request):
    locations_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for place in Place.objects.all():
        locations_data['features'].append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.longitude, place.latitude]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.pk,
                    "detailsUrl": reverse('place_data', args=[place.pk])
                }
            }
        )

    return render(
        request, 'index.html',
        {"locations_data": locations_data}
    )


def place_data(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'), pk=place_id
    )
    images = [image.image.url for image in place.images.all()]

    location_data = {
        "title": place.title,
        "imgs": images,
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude
        },
    }

    response = JsonResponse(
        location_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2}
    )
    response['Content-Type'] = 'application/json; charset=utf-8'

    return response