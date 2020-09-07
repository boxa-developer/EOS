import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse

AUTH_HEADER = {
    'Content-Type': 'application/json'
}


@api_view(['POST'])
def create_task(request):
    data = request.data
    r = requests.post('https://gate.eos.com/api/gdw/'
                      'api?api_key=apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c',
                      headers=AUTH_HEADER, json=data)
    return JsonResponse(r.json(), safe=False)
