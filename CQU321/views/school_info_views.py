from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json
from mycqu.auth import login
from mycqu.mycqu import access_mycqu
from mycqu.course import CQUSessionInfo, CQUSession

import json
from requests import Session


# 获取当前学期
@csrf_exempt
def get_curr_term(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'UserName', 'Password'])
        return_value = {}
        if paras['Statue'] == 1:
            try:
                session = Session()
                login(session, paras['UserName'], paras['Password'])
                access_mycqu(session)
            except:
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'Account Password unmatch'
            else:
                curr_term_info = CQUSessionInfo.fetch(session)
                return_value['Term'] = str(curr_term_info.session)
                return_value['StartDate'] = str(curr_term_info.begin_date)
                return_value['EndDate'] = str(curr_term_info.end_date)
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/school_info_views/get_curr_term.html')


# 获取下一个学期
@csrf_exempt
def get_next_term(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'UserName', 'Password'])
        return_value = {}
        if paras['Statue'] == 1:
            try:
                session = Session()
                login(session, paras['UserName'], paras['Password'])
                access_mycqu(session)
            except:
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'Account Password unmatch'
            else:
                curr_term = CQUSessionInfo.fetch(session)
                next_term_id = curr_term.session.get_id() + 1
                res = session.get(f'https://my.cqu.edu.cn/api/resourceapi/session/info/{next_term_id}')
                data = json.loads(res.content)['data']
                return_value = {
                    'Term': data['year'] + data['term'],
                    'StartDate': data['beginDate'],
                    'EndDate': data['endDate']
                }
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/school_info_views/get_next_term.html')



