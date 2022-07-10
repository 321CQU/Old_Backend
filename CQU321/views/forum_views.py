import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json, connect_db, has_authority
from ..utils.tools import launch_template_data, post_json_analyses, launch_return_data
from CQU321.interface_processing.forum_interface import *


@csrf_exempt
def send_post(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), send_post_process.__name__)
        data = send_post_process(params)
        result = launch_return_data(data, send_post_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('发帖', send_post_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


@csrf_exempt
def update_post(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), update_post_process.__name__)
        data = update_post_process(params)
        result = launch_return_data(data, update_post_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('修改帖子', update_post_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)



@csrf_exempt
def get_post_list(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), get_post_list_process.__name__)
        data = get_post_list_process(params)
        result = launch_return_data(data, get_post_list_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('获取帖子列表', get_post_list_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


@csrf_exempt
def get_post_detail(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), get_post_detail_process.__name__)
        data = get_post_detail_process(params)
        result = launch_return_data(data, get_post_detail_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('获取帖子详情', get_post_detail_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


# 发送回复
@csrf_exempt
def send_reply(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), send_reply_process.__name__)
        data = send_reply_process(params)
        result = launch_return_data(data, send_reply_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('回复帖子', send_reply_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


# 获取评论
@csrf_exempt
def get_reply(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), get_reply_process.__name__)
        data = get_reply_process(params)
        result = launch_return_data(data, get_reply_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('获取帖子回复', get_reply_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


# 删除评论
@csrf_exempt
def delete_reply(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), delete_reply_process.__name__)
        data = delete_reply_process(params)
        result = launch_return_data(data, delete_reply_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('删除帖子回复', delete_reply_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)
