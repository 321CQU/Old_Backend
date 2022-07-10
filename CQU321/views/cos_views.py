import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..utils.tools import launch_template_data, post_json_analyses, launch_return_data
from CQU321.interface_processing.cos_interface import *


@csrf_exempt
def get_cos_credential(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), get_cos_credential_process.__name__)
        data = get_cos_credential_process(params)
        result = launch_return_data(data, get_cos_credential_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('获取对象存储临时访问密钥', get_cos_credential_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)

