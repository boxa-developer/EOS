from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Feature
import requests


AUTH_HEADER = {
    'Authorization':
        'ApiKey apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c',
    'Content-Type': 'application/json'
}


# -------------------------------------------- GET Requests -----------------------------------------------------------
@api_view(['GET'])
def collection(request):
    data = request.data
    print(data)
    print(f'page:{data["page"]} limit:{data["limit"]}')
    r = requests.get(f'https://vt.eos.com/api/data/feature/collection?limit={data["limit"]}&page={data["page"]}', headers=AUTH_HEADER)
    print((r.json()['result'][0]))
    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def history_by_id(request):
    r = requests.get(f'https://vt.eos.com/api/data/feature/{id}/history', headers=AUTH_HEADER)
    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def feature_by_id(request, id):
    r = requests.get(f'https://vt.eos.com/api/data/feature/{id}', headers=AUTH_HEADER)
    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def feature_by_key(request, key):
    r = requests.get(f'https://vt.eos.com/api/data/feature?key={key}')
    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def feature_by_point(request, point):
    r = requests.get(f'https://vt.eos.com/api/data/feature?point={point}')
    return JsonResponse(r.json(), safe=False)


# ------------------------------------------- POST Requests -----------------------------------------------------------
@api_view(['POST'])
def create_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    get_f = requests.get(f'https://vt.eos.com/api/data/feature/{r.json()["id"]}', headers=AUTH_HEADER)
    print(get_f.json()['version'])
    feature = Feature(f_id=r.json()["id"], feature_version=get_f.json()['version'], feature_message=data['message'], data=get_f.json())
    feature.save(force_insert=True)
    return JsonResponse(r.json(), safe=False)


@api_view(['POST'])
def modify_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    return JsonResponse(r.json(), safe=False)


@api_view(['POST'])
def delete_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    return JsonResponse(r.json(), safe=False)