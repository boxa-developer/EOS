from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests

AUTH_HEADER = {
    'Content-Type': 'application/json'
}
api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'


@api_view(['POST'])
def weather_forecast_data(request):
    data = request.data

    url = f'https://gate.eos.com/api/forecast/weather/forecast/?api_key={api_key}'
    r = requests.post(url,headers= AUTH_HEADER, json=data)

    return JsonResponse(r.json(), safe=False)


