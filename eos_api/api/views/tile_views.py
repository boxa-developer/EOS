from typing import Dict

from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
import requests


api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'
AUTH_HEADER: Dict[str, str] = {
    'Content-Type': 'application/json'
}


@api_view(['GET'])
def multi_spectral_tile(request):
    data = request.data
    url = f'https://gate.eos.com/api/render/{data["view_id"]}/' \
          f'{data["bands"]}/{data["z"]}/{data["x"]}/{data["y"]}?api_key={api_key}'
    r = requests.get(url, json=data, headers=AUTH_HEADER)
    print(r.url)
    return Response(r)

