from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

AUTH_HEADER = {
    'Authorization':
        'ApiKey apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c',
    'Content-Type': 'application/json'
}


# -------------------------------------------- GET Requests -----------------------------------------------------------
@api_view(['GET'])
def collection(request, limit, page):
    r = requests.get(f'https://vt.eos.com/api/data/feature/collection?limit={limit}&page={page}', headers=AUTH_HEADER)
    return Response(r)


@api_view(['GET'])
def history_by_id(request):
    r = requests.get(f'https://vt.eos.com/api/data/feature/{id}/history', headers=AUTH_HEADER)
    return Response(r)


@api_view(['GET'])
def feature_by_id(request, id):
    r = requests.get(f'https://vt.eos.com/api/data/feature/{id}', headers=AUTH_HEADER)
    return Response(r)


@api_view(['GET'])
def feature_by_key(request, key):
    r = requests.get(f'https://vt.eos.com/api/data/feature?key={key}')
    return Response(r)


@api_view(['GET'])
def feature_by_point(request, point):
    r = requests.get(f'https://vt.eos.com/api/data/feature?point={point}')
    return Response(r)


# ------------------------------------------- POST Requests -----------------------------------------------------------
@api_view(['POST'])
def create_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    return Response(r.content)


@api_view(['POST'])
def modify_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    return Response(r.content)


@api_view(['POST'])
def delete_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    return Response(r.content)
