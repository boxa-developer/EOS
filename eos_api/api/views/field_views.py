from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db import IntegrityError
import requests

AUTH_HEADER = {
    'Content-Type': 'application/json'
}
api_key = 'apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'


@api_view(['GET'])
def field_by_point(request):
    point = request.GET.get('point')
    url = f'https://gate.eos.com/api/cz/backend/api/field/{point}?api_key={api_key}'
    r = requests.get(url, headers=AUTH_HEADER)

    return JsonResponse((r.json()), safe=False)
