from typing import Dict

from rest_framework.decorators import api_view
from django.http import JsonResponse
# from rest_framework.response import Response
import requests


api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'
AUTH_HEADER: Dict[str, str] = {
    'Content-Type': 'application/json'
}


@api_view(['GET'])
def multi_spectral_tile(request):
    print(f'ENtered: {request.GET.get("url")}')
    url = request.GET.get("url")
    urlx = f'https://gate.eos.com/api/render/{url}?api_key={api_key}'
    r = requests.get(urlx, headers=AUTH_HEADER)
    return JsonResponse(r.url, safe=False)


@api_view(['GET'])
def virtual_band_tile(request):
    url = request.GET.get("url")
    urlx = f'https://gate.eos.com/api/render/{url}?api_key={api_key}'
    r = requests.get(urlx, headers=AUTH_HEADER)
    return JsonResponse(r.url, safe=False)


@api_view(['GET'])
def terrain(request):
    url = request.GET.get("url")
    urlx = f'https://gate.eos.com/api/render/terrain/{url}?api_key={api_key}'
    print(urlx)
    r = requests.get(urlx, headers=AUTH_HEADER)
    return JsonResponse(r.url, safe=False)

