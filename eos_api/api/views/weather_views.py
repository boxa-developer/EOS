from typing import Dict
from django.db import connection
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
from ..models import EFeature

AUTH_HEADER: Dict[str, str] = {
    'Content-Type': 'application/json'
}
api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'


@api_view(['POST'])
def weather_forecast_data(request):
    data = request.data

    url = f'https://gate.eos.com/api/forecast/weather/forecast/?api_key={api_key}'
    r = requests.post(url, headers=AUTH_HEADER, json=data)

    return JsonResponse(r.json(), safe=False)


@api_view(['POST'])
def weather_forecast(request):
    data = request.data

    url = f'https://gate.eos.com/api/forecast/weather/forecast/world/?api_key={api_key}'
    r = requests.post(url, headers=AUTH_HEADER, json=data)

    return JsonResponse(r.json(), safe=False)


@api_view(['POST'])
def weather_history(request):
    data = request.data
    print(request.data)
    export_data = weather_data(data["polygon_id"])
    if export_data != None:
        send_data = dict()
        send_data = {
            "geometry": export_data[0],
            "start_date": data["start_date"],
            "end_date": data["end_date"]
        }

        url = f'https://gate.eos.com/api/cz/backend/forecast-history/?api_key={api_key}'
        r = requests.post(url, headers=AUTH_HEADER, json=send_data)
        print(r.json())
        return JsonResponse(r.json(), safe=False)
    else:
        return JsonResponse('Id mavjum emas!', safe=False)


# {'polygon_id': ['1'], 'start_date': ['2020-07-20'], 'end_date': ['2020-08-22']}

def weather_data(pk_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT feature_data::json->'geometry' FROM api_efeature  WHERE export_id={};
            """.format(pk_id)
        )
        row = cursor.fetchone()
    return row

def my_custom_sql(t_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT "
                       "ST_AsGeoJSON(ST_Transform(way,3857))::json -> 'coordinates'"
                       " FROM agromonitoring.polygons2 "
                       "WHERE id = 1;")

        row = cursor.fetchone()

    return row
