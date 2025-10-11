from django.shortcuts import render

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
                    "detailsUrl": ""
                }
            }
        )

    return render(request, 'index.html', {"locations_data": locations_data})