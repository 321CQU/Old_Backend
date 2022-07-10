import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..utils.tools import launch_template_data, post_json_analyses, launch_return_data
from CQU321.interface_processing.announcement_interface import *


@csrf_exempt
def get_group_info(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), get_group_info_process.__name__)
        info = get_group_info_process(params)
        result = launch_return_data(info, get_group_info_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('查询组织信息', get_group_info_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


@csrf_exempt
def get_announcement_list(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), get_announcement_list_process.__name__)
        announcements = get_announcement_list_process(params)
        result = launch_return_data(announcements, get_announcement_list_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('查询活动公告列表', get_announcement_list_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


@csrf_exempt
def get_announcement_detail(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), get_announcement_detail_process.__name__)
        markdown = get_announcement_detail_process(params)
        result = launch_return_data(markdown, get_announcement_detail_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('查询活动公告正文', get_announcement_detail_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


@csrf_exempt
def subscribe_group(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), subscribe_group_process.__name__)
        res = subscribe_group_process(params)
        result = launch_return_data(res, subscribe_group_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('关注/取关组织', subscribe_group_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)

@csrf_exempt
def subscribe_list(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), subscribe_list_process.__name__)
        res = subscribe_list_process(params)
        result = launch_return_data(res, subscribe_list_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('获取关注的组织列表', subscribe_list_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)
