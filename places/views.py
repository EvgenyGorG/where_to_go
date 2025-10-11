from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from places.models import Place


def place_data(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'), pk=place_id
    )
    images = [image.image.url for image in place.images.all()]

    data = {
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
        data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2}
    )
    response['Content-Type'] = 'application/json; charset=utf-8'

    return response
