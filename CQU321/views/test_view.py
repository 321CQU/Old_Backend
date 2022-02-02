from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json

import json


@csrf_exempt
def test_data(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Data'])
        return_value = {'Statue': 1}
        for key, value in paras['Data'].items():
            return_value[key] = value
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/test_views/test_data.html')
