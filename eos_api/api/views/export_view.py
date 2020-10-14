from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geojson_rewind import rewind
from ..models import EFeature
import requests, json

AUTH_HEADER = {
    'Authorization':
        'ApiKey apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c',
    'Content-Type': 'application/json'
}


@api_view(['GET'])
def export_features(request):
    query_data = import_geometry()
    # print(query_data)
    for data in query_data:
        idx, properties, cords, create_date, \
        fermer_id, crop_type, contour_number, area = data
        raw_data = dict()
        raw_data = {
            "action": "create",
            # "key": f"eos-project-by-fizmasoft-{idx}",
            "type": "Feature",
            "message": "eos project by fizmasoft",
            "properties": {
                "name": "everything ok!"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": cords
            }
        }

        raw_data['geometry'] = rewind(raw_data['geometry'])

        post_url = 'https://vt.eos.com/api/data/feature/'
        r = requests.post(post_url, headers=AUTH_HEADER, json=raw_data)

        get_url = f'https://vt.eos.com/api/data/feature/{r.json()["id"]}'
        get_f = requests.get(get_url, headers=AUTH_HEADER)

        try:
            feature = EFeature(export_id=idx,
                               farmer_id=fermer_id,
                               polygon=json.dumps(cords),
                               feature_data=get_f.json(),
                               properties=properties,
                               crop_type=1,
                               contour_number=1)
            feature.save(force_insert=True)
        except Exception as e:
            print(e)

    return Response(query_data)


def import_geometry():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT "
            "id, "
            "properties, "
            "ST_AsGeoJSON(ST_Transform(way,4326))::json -> 'coordinates',"
            "created_date,"
            "fermer_id,"
            "crop_type,"
            "contour_number,"
            "ST_Area(way)"
            "FROM agromonitoring.polygons2;"
        )

        rows = cursor.fetchall()
    return rows

