from typing import Dict

from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
import requests

AUTH_HEADER: Dict[str, str] = {
    'Content-Type': 'application/json'
}

api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'


@api_view(['POST'])
def search(request):

    data = request.data
    post_url = f'https://hlv.eos.com/api/v1/search?api_key={api_key}'
    r = requests.post(post_url, headers=AUTH_HEADER, json=data)

    return JsonResponse(r.json(), safe=False)


@api_view(['POST'])
def single_search(request, dataset_id):

    data = request.data
    post_url = f'https://gate.eos.com/api/lms/search/v2/{dataset_id}?api_key={api_key}'
    r = requests.post(post_url, headers=AUTH_HEADER, json=data)

    return JsonResponse(r.json(), safe=False)


@api_view(['POST'])
def multi_search(request):

    data = request.data
    post_url = f'https://gate.eos.com/api/lms/search/v2?api_key={api_key}'
    r = requests.post(post_url, headers=AUTH_HEADER,
                      json=data)

    return JsonResponse(r.json(), safe=False)
