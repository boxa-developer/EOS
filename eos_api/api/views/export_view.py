from rest_framework.decorators import api_view
from rest_framework.response import Response
from geojson_rewind import rewind
from ..models import EFeature
import requests, json
from django.http import JsonResponse
from .query import query_one,query_many

AUTH_HEADER = {
    'Authorization':
        'ApiKey apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c',
    'Content-Type': 'application/json'
}
api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'


@api_view(['GET'])
def export_features(request):
    query_data = query_many(
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
            feature = EFeature(farmer_id=fermer_id,
                               way=way,
                               feature_data=get_f.json(),
                               properties=properties,
                               crop_type=crop_type,
                               contour_number=contour_number)
            feature.save(force_insert=True)
        except Exception as e:
            print(e)
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
    send_data = query_one("""SELECT
                        json_build_object('type', 'FeatureCollection', 'features', 
                            json_agg(ST_AsGeoJson(ST_Transform(way, 4326))::jsonb || jsonb_build_object('properties',
                             jsonb_build_object('id', feature_data->'id', 'pid', id) || properties))
                        ) as res
                    FROM api_efeature 
                    WHERE farmer_id = '{}';""".format(data["fermer_id"]))
    return JsonResponse(send_data[0], safe=False)


