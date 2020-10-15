from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geojson_rewind import rewind
from ..models import EFeature
import requests, json
from django.http import JsonResponse

AUTH_HEADER = {
    'Authorization':
        'ApiKey apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c',
    'Content-Type': 'application/json'
}
api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'

@api_view(['GET'])
def export_features(request):
    query_data = import_geometry()
    # print(query_data)
    for data in query_data:
        idx, properties, cords, create_date, fermer_id, crop_type, contour_number, area, way = data
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
                               way=way,
                               feature_data=get_f.json(),
                               properties=properties,
                               crop_type=crop_type,
                               contour_number=contour_number)
            feature.save(force_insert=True)
        except Exception as e:
            print(e)
    # https: // gate.eos.com / api / render / cropper /?api_key = XXX
    return Response(query_data)


@api_view(['GET'])
def set_cropper_refs(request):
    features = EFeature.objects.all()
    for feature in features:
        geometry = feature.feature_data["geometry"]
        cropper_request = requests.post(
            url=f"https://gate.eos.com/api/render/cropper/?api_key={api_key}",
            json={"geometry": geometry}
        )
        cpr = cropper_request.json()["cropper_ref"]
        feature.cropper_ref = cpr
        feature.save()
    return Response("Done")
@api_view(['POST'])
def get_geojson(request):
    data = request.data
    send_data = get_features_collection(farmer_id=data["fermer_id"])
    return JsonResponse(send_data[0], safe=False)


def get_features_collection(farmer_id=4):
    query_str = """SELECT
                        json_build_object('type', 'FeatureCollection', 'features', 
                            json_agg(ST_AsGeoJson(ST_Transform(way, 4326))::jsonb || jsonb_build_object('properties',
                             jsonb_build_object('id', feature_data->'id', 'pid', id) || properties))
                        ) as res
                    FROM api_efeature 
                    WHERE farmer_id = '{}';""".format(farmer_id)

    with connection.cursor() as cursor:
        cursor.execute(
            query_str
        )
        row = cursor.fetchone()
    return row


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
            "ST_Area(way), way "
            "FROM agromonitoring.polygons2;"
        )

        rows = cursor.fetchall()
    return rows
