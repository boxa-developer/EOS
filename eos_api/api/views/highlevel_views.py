from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests

AUTH_HEADER = {
    'Content-Type': 'application/json'
}
api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'


@api_view(['GET'])
def statistics(request):
    stat_id = request.GET.get('stat_id')
    url = f'https://hlv.eos.com/api/v1/results/stats/{stat_id}?api_key={api_key}'
    r = requests.get(url, headers=AUTH_HEADER)
    print(r.url)
    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def download(request):
    stat_id = request.GET.get('download_id')
    url = f'https://hlv.eos.com/api/v1/results/image/{stat_id}?api_key={api_key}'
    r = requests.get(url, headers=AUTH_HEADER)
    print(r.url)
    return JsonResponse(r.json(), safe=False)
