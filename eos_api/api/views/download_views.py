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


@api_view(['GET'])
def get_visual(request):
    data = request.data
    geometry, feature_id = query_one("""
            SELECT 
                feature_data::json->'geometry',
                feature_data::json->'id'  
            FROM api_efeature  
            WHERE id={};
            """.format(data["pid"]))

    search_data = {
        "date": {
            "from": "2019-01-20",
            "to": "2019-10-15"
        },
        "bm_type": ["NDVI"],
        "satellites": ["landsat8"],
        "polygon_id": str(feature_id),
        "limit": 1
    }
    search_request = requests.post(
        url=f'https://hlv.eos.com/api/v1/search?api_key={api_key}',
        json=search_data,
        headers=AUTH_HEADER)
    view_id = search_request.json()["results"][0]["view_id"]
    url = "https://gate.eos.com/api/render/{}/(NIR-RED)/(" \
          "NIR+RED)/{{z}}/{{x}}/{{y}}?cropper_ref=95208741efc3bf735048895605e206ca&COLORMAP" \
          "={}".format(
        view_id, color_map)
    send_data = {
        "url": url,
        "id": data["pid"]
    }
    return JsonResponse(send_data, safe=False)


@api_view(['POST'])
def get_images(request):
    data = request.data
    geometry, feature_id = query_one("""
                SELECT 
                    feature_data::json->'geometry',
                    feature_data::json->'id'  
                FROM api_efeature  
                WHERE id={};
                """.format(data["pid"]))

    search_data = {
        "date": {
            "from": "2019-01-20",
            "to": "2019-10-15"
        },
        "bm_type": ["NDVI"],
        "satellites": ["landsat8"],
        "polygon_id": str(feature_id),
        "limit": 1
    }
    search_request = requests.post(
        url=f'https://hlv.eos.com/api/v1/search?api_key={api_key}',
        json=search_data,
        headers=AUTH_HEADER)
    view_id = search_request.json()["results"][0]["view_id"]

    post_data = {
        "type": "jpeg",
        "params": {
            "view_id": view_id,
            # "bm_type": "(B5-B4)/(B5+B4)",
            "bm_type": "NDVI",
            "geometry": geometry,
            "px_size": 2,
            "format": "png",
            "colormap": f"{color_map}",
            "reference": "ref_datetime"
        }
    }

    visual_request = requests.post(
        url=f'https://gate.eos.com/api/gdw/api?api_key={api_key}',
        json=post_data,
        headers=AUTH_HEADER)
    url_data = {
        "url": f"https://gate.eos.com/api/gdw/api/{visual_request.json()['task_id']}?api_key={api_key}"
    }
    return JsonResponse(url_data, safe=False)
