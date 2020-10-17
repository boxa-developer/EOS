from typing import Dict
from django.db import connection
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import requests
from .query import query_one

AUTH_HEADER: Dict[str, str] = {
    'Content-Type': 'application/json'
}

api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'
color_map = "2b0040e4100279573a41138c8a30c1f2&api_key=apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c"


@api_view(['POST'])
def get_visual(request):
    data = request.data
    geometry, feature_id,crp = query_one("""
            SELECT 
                feature_data::json->'geometry',
                feature_data::json->'id', 
                cropper_ref  
            FROM api_efeature  
            WHERE id={};
            """.format(data["pid"]))

    search_data = {
        "date": {
            "from": "2019-01-20",
            "to": "2020-10-15"
        },
        "bm_type": ["NDVI"],
        "satellites": ["sentinel2"],
        "polygon_id": str(feature_id),
    }
    search_request = requests.post(
        url=f'https://hlv.eos.com/api/v1/search?api_key={api_key}',
        json=search_data,
        headers=AUTH_HEADER)
    # view_id = search_request.json()["results"][0]["view_id"]
    # url = "https://gate.eos.com/api/render/{}/(NIR-RED)/(" \
    #       "NIR+RED)/{{z}}/{{x}}/{{y}}?cropper_ref={}&COLORMAP" \
    #       "={}".format(
    #     view_id, crp,color_map)
    # send_data = {
    #     "url": url,
    #     "id": data["pid"]
    # }
    return JsonResponse(search_request.json(), safe=False)


@api_view(['POST'])
def get_images(request):
    data = request.data
    geometry, feature_id, bounding_box, cpr = query_one("""
                SELECT 
                    feature_data::json->'geometry',
                    feature_data::json->'id' ,
                    Box2d(ST_Transform(way, 4326)),
                    cropper_ref 
                FROM api_efeature  
                WHERE id={};
                """.format(data["pid"]))


    search_data = {
        "search": {
            "satellites": ["sentinel2"],
            "date": {
                "from": "2018-08-20"
            },

            "shape": geometry,

        },
        "limit": 1,
        "fields": ["date"]
    }
    search_request = requests.post(
        url=f'https://gate.eos.com/api/lms/search/v2?api_key={api_key}',
        json=search_data,
        headers=AUTH_HEADER)
    # view_id = search_request.json()["results"][0]["view_id"]
    #
    # bounding_box = [(bounding_box.split("(")[1].split(")")[0].split(",")[i].split(" "))
    #                 for i in range(len(bounding_box.split("(")[1].split(")")[0].split(",")))]
    # import math
    # aspect_ratio = math.fabs((eval(bounding_box[0][0])-eval(bounding_box[1][0]))/(eval(bounding_box[0][1])-eval(bounding_box[1][1])))
    # w = int(250*aspect_ratio)
    # url = f"https://render.eosda.com/{view_id}/(NIR-RED)/(" \
    #       f"NIR+RED)/16/{bounding_box[0][0]};{bounding_box[1][0]};" \
    #       f"4326/{bounding_box[0][1]};{bounding_box[1][1]};4326?COLORMAP" \
    #       "=2b0040e4100279573a41138c8a30c1f2&MASK_COLOR=ffffff&MASKING=CLOUD&MIN_MAX=0," \
    #       f"1&cropper_ref={cpr}&TILE_SIZE={w},250&CALIBRATE=1 "

    return JsonResponse(search_request.json(), safe=False)
