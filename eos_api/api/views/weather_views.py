from typing import Dict
from django.db import connection
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
from ..models import EFeature
from .query import query_one

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
    export_data = query_one("""
            SELECT 
                feature_data::json->'geometry' 
            FROM api_efeature  
            WHERE id={};
            """.format(data["polygon_id"]))

    if export_data is not None:
        send_data = dict()
        send_data = {
            "geometry": export_data[0],
            "start_date": data["start_date"],
            "end_date": data["end_date"]
        }

        url = f'https://gate.eos.com/api/cz/backend/forecast-history/?api_key={api_key}'
        r = requests.post(url, headers=AUTH_HEADER, json=send_data)
        print(r.json())

        chart_data = {
            "x": [r.json()[i]["date"] for i in range(len(r.json()))],
            "min": [float(r.json()[i]["temperature_min"]) for i in range(len(r.json()))],
            "max": [float(r.json()[i]["temperature_max"]) for i in range(len(r.json()))],
            "veg": [float(r.json()[i]["rainfall"]) for i in range(len(r.json()))],
        }

        return JsonResponse(chart_data, safe=False)
    else:
        return JsonResponse('Id mavjum emas!', safe=False)
