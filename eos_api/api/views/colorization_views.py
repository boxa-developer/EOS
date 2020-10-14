from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests

AUTH_HEADER = {
    'Content-Type': 'application/json'
}
api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'


@api_view(['GET'])
def all_colormap(request):
    url = f'https://gate.eos.com/api/render/colormap/ALL?api_key=a{api_key}'
    r = requests.get(url, headers=AUTH_HEADER)
    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def colormap_by_id(request):
    color_id = request.GET.get('color_id')
    url = f'https://gate.eos.com/api/render/colormap/{color_id}?api_key={api_key}'
    r = requests.get(url, headers=AUTH_HEADER)
    return JsonResponse(r.json(), safe=False)
