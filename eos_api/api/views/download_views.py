from typing import Dict
from django.db import connection
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import requests
from ..models import EFeature

AUTH_HEADER: Dict[str, str] = {
    'Content-Type': 'application/json'
}

api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'


@api_view(['GET'])
def get_visual(request):
    data = request.data
    geometry, feature_id = get_geometry(data["pid"])
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
          "=2b0040e4100279573a41138c8a30c1f2&api_key=apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c".format(
        view_id)
    send_data = {
        "url": url,
        "id": data["pid"]
    }
    return JsonResponse(send_data, safe=False)


def get_geometry(pk_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT feature_data::json->'geometry',feature_data::json->'id'  FROM api_efeature  WHERE id={};
            """.format(pk_id)
        )
        row = cursor.fetchone()
    return row
