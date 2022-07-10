import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..CQUGetter_old import CQUGetter
from ..tools import analysis_json
from ..utils.tools import launch_template_data, post_json_analyses, launch_return_data
from CQU321.interface_processing.library_interface import search_book_process, get_book_pos_process


@csrf_exempt
def get_borrow_list(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'UserName', 'Password', 'IsCurr'])
        return_value = {}
        if paras['Statue'] == 1:
            getter = CQUGetter()
            if getter.is_match(paras['UserName'], paras['Password']):
                return_value['BookList'] = getter.get_borrow_list(paras['IsCurr'])
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'Account password unmatch'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/library_views/get_borrow_list.html')


@csrf_exempt
def renew_book(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'UserName', 'Password', 'BookId'])
        return_value = {}
        if paras['Statue'] == 1:
            getter = CQUGetter()
            if getter.is_match(paras['UserName'], paras['Password']):
                is_success, info = getter.renew_book(paras['BookId'])
                if is_success:
                    return_value['Info'] = info
                else:
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 2
                    paras['ErrorInfo'] = 'Library Refuse, error info: ' + info
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 3
                paras['ErrorInfo'] = 'Account password unmatch'

        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/library_views/renew_book.html')


@csrf_exempt
def search_book(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), search_book_process.__name__)
        search_list = search_book_process(params)
        result = launch_return_data(search_list, search_book_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('根据关键词搜索书籍信息', search_book_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


@csrf_exempt
def get_book_pos(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), get_book_pos_process.__name__)
        search_list = get_book_pos_process(params)
        result = launch_return_data(search_list, get_book_pos_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('根据书籍id搜索书籍借阅信息', get_book_pos_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)

