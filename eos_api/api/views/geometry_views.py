from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import Feature
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

    url = f'https://vt.eos.com/api/data/feature/collection?limit={data["limit"]}&page={data["page"]}'
    r = requests.get(url, headers=AUTH_HEADER)

    for ft in r.json()['result']:
        try:
            ftr = Feature(f_id=ft['id'], feature_version=ft['version'], data=ft)
            ftr.save()
        except IntegrityError as e:
            pass

    return JsonResponse((r.json()['result']), safe=False)


@api_view(['GET'])
def all_features(request):
    features = Feature.objects.all()

    f_coll = {
        'count': len(features),
        'features': []
    }
    for ftr in features:
        f_coll['features'].append(
            ftr.data
        )

    return JsonResponse(f_coll, safe=False)


@api_view(['GET'])
def history_by_id(request, id):
    url = f'https://vt.eos.com/api/data/feature/{id}/history'
    r = requests.get(url, headers=AUTH_HEADER)

    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def feature_by_id(request, id):
    url = f'https://vt.eos.com/api/data/feature/{id}'
    r = requests.get(url, headers=AUTH_HEADER)

    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def feature_by_key(request, key):
    print(key)
    url = f'https://vt.eos.com/api/data/feature?key={key}'
    r = requests.get(url, headers=AUTH_HEADER)

    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def feature_by_geometry(request):
    if request.GET.get('point') is not None:
        url = f'https://vt.eos.com/api/data/feature?point={request.GET.get("point")}'
        r = requests.get(url, headers=AUTH_HEADER)
        return JsonResponse(r.json(), safe=False)
    elif request.GET.get('bbox') is not None:
        url = f'https://vt.eos.com/api/data/feature?bbox={request.GET.get("bbox")}'
        r = requests.get(url, headers=AUTH_HEADER)
        return JsonResponse(r.json(), safe=False)
    else:
        return JsonResponse("Something Went Wrong Check Arguments!", safe=False)


# ------------------------------------------- POST Requests -----------------------------------------------------------
@api_view(['POST'])
def create_feature(request):
    data = request.data

    post_url = 'https://vt.eos.com/api/data/feature/'
    r = requests.post(post_url, headers=AUTH_HEADER, json=data)

    get_url = f'https://vt.eos.com/api/data/feature/{r.json()["id"]}'
    get_f = requests.get(get_url, headers=AUTH_HEADER)

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

    post_url = 'https://vt.eos.com/api/data/feature/'
    r = requests.post(post_url, headers=AUTH_HEADER, json=data)

    get_url = f'https://vt.eos.com/api/data/feature/{r.json()["id"]}'
    get_f = requests.get(get_url, headers=AUTH_HEADER)

    try:
        feature = Feature.objects.get(f_id=r.json()["id"])
        feature.feature_version = get_f.json()['version']
        feature.feature_message = data['message']
        feature.data = get_f.json()
        feature.save()
    except Exception as e:
        print(e)

    return JsonResponse(r.json()['id'], safe=False)


@api_view(['POST'])
def delete_feature(request):
    data = request.data

    url = 'https://vt.eos.com/api/data/feature/'
    r = requests.post(url, headers=AUTH_HEADER, json=data)
    f_id = r.json()['id']

    try:
        Feature.objects.get(f_id=f_id).delete()
    except Exception as e:
        print(e)

    return JsonResponse(r.json()['id'], safe=False)


@api_view(['GET'])
def delete_all_features(request):
    url = f'https://vt.eos.com/api/data/feature/collection?limit=500&page=1'
    r = requests.get(url, headers=AUTH_HEADER)
    ids = []
    for _ in r.json()['result']:
        ids.append(_['id'])

    for ix in ids:
        data = {
            "action": "delete",
            "id": ix,
            "version": 1,
            "type": "Feature",
            "message": "Deleted",
            "properties": {"name": "Editted Text", "shop": True},
            "geometry": {
                "type": "Point",
                "coordinates": [1, 1]
            }
        }
        url = 'https://vt.eos.com/api/data/feature/'
        r = requests.post(url, headers=AUTH_HEADER, json=data)

    return JsonResponse('Deleted All!', safe=False)
