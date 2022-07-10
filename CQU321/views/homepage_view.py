from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from CQU321.interface_processing.homepage_interface import *
from CQU321.utils.tools import post_json_analyses, launch_return_data, launch_template_data


@csrf_exempt
def homepage(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), homepage_process.__name__)
        urls = homepage_process(params)
        result = launch_return_data(urls, homepage_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('首页图片加载', homepage_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)

