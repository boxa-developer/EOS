from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

AUTH_HEADER = {
    'Authorization':
        'ApiKey apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c',
    'Content-Type': 'application/json'
}


@api_view(['GET'])
def collect_view(request):
    r = requests.get('https://vt.eos.com/api/data/feature/collection?limit=10&page=1', headers=AUTH_HEADER)
    return Response(r)


@api_view(['GET'])
def feature_view(request):
    r = requests.get('https://vt.eos.com/api/data/feature/17068821', headers=AUTH_HEADER)
    return Response(r)


@api_view(['GET'])
def history_view(request):
    r = requests.get('https://vt.eos.com/api/data/feature/17068821/history', headers=AUTH_HEADER)
    return Response(r)


@api_view(['POST'])
def create_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    return Response(r.content)