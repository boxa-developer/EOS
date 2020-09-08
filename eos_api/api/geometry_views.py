from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Feature
from django.db import IntegrityError
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
    r = requests.get(f'https://vt.eos.com/api/data/feature/collection?limit={data["limit"]}&page={data["page"]}',
                     headers=AUTH_HEADER)
    for ft in r.json()['result']:
        try:
            ftr = Feature(f_id=ft['id'], feature_version=ft['version'], data=ft)
            ftr.save()
        except IntegrityError as e:
            pass
    return JsonResponse(len(r.json()['result']), safe=False)


@api_view(['GET'])
def all_features(request):
    features = Feature.objects.all()
    fcoll = {
        'count': len(features),
        'features': []
    }
    for ftr in features:
        fcoll['features'].append(
            ftr.data
        )

    return JsonResponse(collection, safe=False)


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
    try:
        feature = Feature(f_id=r.json()["id"], feature_version=get_f.json()['version'],
                          feature_message=data['message'], data=get_f.json())
        feature.save(force_insert=True)
    except Exception as e:
        print(e)
    return JsonResponse(r.json(), safe=False)


@api_view(['POST'])
def modify_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    get_f = requests.get(f'https://vt.eos.com/api/data/feature/{r.json()["id"]}', headers=AUTH_HEADER)
    try:
        # print(f'id:{r.json()["id"]}')
        feature = Feature.objects.get(f_id=r.json()["id"])
        feature.feature_version = get_f.json()['version']
        feature.feature_message = data['message']
        feature.data = get_f.json()
        feature.save()
    except Exception as e:
        print(e)

    return JsonResponse(r.json(), safe=False)


@api_view(['POST'])
def delete_feature(request):
    data = request.data
    r = requests.post('https://vt.eos.com/api/data/feature/', headers=AUTH_HEADER, json=data)
    id = r.json()['id']
    try:
        Feature.objects.get(f_id=id).delete()
    except Exception as e:
        print(e)
    return JsonResponse(r.json(), safe=False)
