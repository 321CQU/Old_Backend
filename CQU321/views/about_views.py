from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json
from Website.settings import BASE_DIR

import json


@csrf_exempt
def about_us(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key'])
        return_value = {}
        if paras['Statue'] == 1:
            with open(str(BASE_DIR) + '/templates/321CQU/md/about_us.md', 'r') as f:
                content = f.read()
            return_value['Content'] = content
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/about_views/about_us.html')


@csrf_exempt
def get_tutorials(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key'])
        return_value = {}
        if paras['Statue'] == 1:
            with open(str(BASE_DIR) + '/templates/321CQU/md/tutorials.md', 'r') as f:
                content = f.read()
            return_value['Content'] = content
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/about_views/get_tutorials_views.html')

