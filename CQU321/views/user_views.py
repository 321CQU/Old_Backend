from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..CQUGetter import CQUGetter
from ..tools import analysis_json, get_code, connect_db

import json
import re


# 设置用户昵称、头像
@csrf_exempt
def set_info(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'UserName', 'UserImg'])
        connection, cursor = connect_db()
        res = re.match(r'[\u4E00-\u9FA5]+', paras['Sid'])
        return_value = {}
        if res is not None:
            paras['Statue'] = 0
            paras['ErrorCode'] = 2
            paras['ErrorInfo'] = 'Uncorrected Sid'
        if paras['Statue'] == 1:
            try:
                if paras['UserName'] == '':
                    sql = 'update UserInfo set UserName = null where Sid = %s'
                    cursor.execute(sql, (paras['Sid'],))
                else:
                    sql = 'update UserInfo set UserName = %s where Sid = %s'
                    cursor.execute(sql, (paras['UserName'], paras['Sid']))
                if paras['UserImg'] == '':
                    sql = 'update UserInfo set UserImg = null where Sid = %s'
                    cursor.execute(sql, (paras['Sid'],))
                else:
                    sql = 'update UserInfo set UserImg = %s where Sid = %s'
                    cursor.execute(sql, (paras['UserImg'], paras['Sid']))
                connection.commit()
            except:
                connection.rollback()
                paras['Statue'] = 0
                paras['ErrorCode'] = 3
                paras['ErrorInfo'] = 'Sql execute error'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/user_views/set_user_info.html')


# 校验本科生账号密码是否正确
@csrf_exempt
def is_match(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'UserName', 'Password', 'Code', 'NeedAll'], ['Debug'])
        connection, cursor = connect_db()
        res = re.match(r'[\u4E00-\u9FA5]+', paras['Sid'])
        if res is not None:
            paras['Statue'] = 0
            paras['ErrorCode'] = 2
            paras['ErrorInfo'] = 'Uncorrected Sid'
        return_value = {}
        if paras['Statue'] == 1:
            getter = CQUGetter(sid=paras['Sid'])
            if getter.is_match(paras['UserName'], paras['Password']):
                if paras['NeedAll']:
                    pass
                    if 'Debug' in paras:
                        open_id = paras['Debug']
                    else:
                        open_id = get_code(paras['Code'])
                    if open_id is not None:
                        score_log = getter.get_score(connection, cursor, open_id, True)
                        if score_log is not None:
                            return_value['ScoreLog'] = score_log
                        else:
                            paras['Statue'] = 0
                            paras['ErrorCode'] = 3
                            paras['ErrorInfo'] = 'There is no score information about this student'
                    else:
                        paras['Statue'] = 0
                        paras['ErrorCode'] = 4
                        paras['ErrorInfo'] = 'Openid acquisition error'
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 5
                paras['ErrorInfo'] = 'Account password unmatch'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/user_views/is_match.html')

