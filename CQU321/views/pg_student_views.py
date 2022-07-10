from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..CQUGetter_old import CQUGetter
from ..tools import analysis_json

import json
import re

@csrf_exempt
def pg_is_match(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'UserName', 'Password'])
        return_value = {}
        if paras['Statue'] == 1:
            if re.search(r'^[0-9]{12}t?', paras['UserName']):
                getter = CQUGetter()
                if not getter.pg_is_match(paras['UserName'], paras['Password']):
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 2
                    paras['ErrorInfo'] = 'Account password unmatch'
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 3
                paras['ErrorInfo'] = 'Uncorrected Account'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/pg_student_views/pg_is_match.html')


@csrf_exempt
def pg_get_score(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'UserName', 'Password'])
        return_value = {}
        if paras['Statue'] == 1:
            if re.search(r'^[0-9]{12}t?', paras['UserName']):
                getter = CQUGetter()
                if getter.pg_is_match(paras['UserName'], paras['Password']):
                    score_log = getter.pg_get_score()
                    if score_log is not None:
                        return_value['ScoreLog'] = score_log
                else:
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 2
                    paras['ErrorInfo'] = 'Account password unmatch'
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 3
                paras['ErrorInfo'] = 'Uncorrected Account'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/pg_student_views/pg_get_score.html')
