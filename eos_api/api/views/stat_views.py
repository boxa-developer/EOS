import requests
from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import Task

AUTH_HEADER = {
    'Content-Type': 'application/json'
}


@api_view(['POST'])
def create_task(request):
    data = request.data

    url = 'https://gate.eos.com/api/gdw/' \
          'api?api_key=apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'
    r = requests.post(url ,
                      headers=AUTH_HEADER, json=data)
    r_data = r.json()

    try:
        task = Task(task_id=r_data['task_id'], status=r_data['status'],
                    req_id=r_data['req_id'], task_timeout=r_data['task_timeout'])
        task.save()
    except Exception as e:
        print(e)

    return JsonResponse(r.json(), safe=False)


@api_view(['GET'])
def check_status(request, task_id):
    try:
        url = f'https://gate.eos.com/api/gdw/api/{task_id}'\
                '?api_key=apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c'
        r = requests.get(url, headers=AUTH_HEADER)

        task = Task.objects.get(task_id=task_id)
        task.data = r.json()
        task.save()
        return JsonResponse("ok", safe=False)
    except Exception as e:
        print(e)
