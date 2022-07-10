from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..CQUGetter_old import CQUGetter
from ..tools import analysis_json, get_code, connect_db

from CQU321.interface_processing.user_interface import *
from CQU321.utils.tools import post_json_analyses, launch_return_data, launch_template_data

import json
import re


@csrf_exempt
def binding_auth(request):
    if request.method == 'POST' and request.body:
        params = post_json_analyses(request.body.decode('utf-8'), binding_auth_process.__name__)
        res = binding_auth_process(params)
        result = launch_return_data(res, binding_auth_process.__name__)
        return JsonResponse(result)
    elif request.method == 'GET':
        version = request.GET.get('version')
        sections = launch_template_data('绑定统一身份认证行号', binding_auth_process.__name__, version)
        return render(request, '321CQU/api_template.html', context=sections)


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

                sql = 'select Authority from UserInfo where Sid = %s'
                cursor.execute(sql, (paras['Sid'],))
                return_value['Authority'] = cursor.fetchone()[0]
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


@csrf_exempt
def is_match(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'UserName', 'Password'], ['Debug'])
        return_value = {}
        if paras['Statue'] == 1:
            getter = CQUGetter()
            if getter.is_match(paras['UserName'], paras['Password']):
                return_value = getter.get_person_info()
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


@csrf_exempt
def after_advertise(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Code'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            open_id = get_code(paras['Code'])
            if open_id is not None:
                sql = 'call Advertise_add(%s)'
                try:
                    cursor.execute(sql, (open_id,))
                except:
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 2
                    paras['ErrorInfo'] = 'sql execute error'
                    connection.rollback()
                else:
                    connection.commit()
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 3
                paras['ErrorInfo'] = 'Openid acquisition error'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/user_views/advertise.html')


@csrf_exempt
def get_advertise_times(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Code'], ['Debug'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            open_id = get_code(paras['Code'])
            if open_id is not None:
                sql = 'select times from Advertisement where Openid = %s'
                try:
                    cursor.execute(sql, (open_id,))
                except:
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 2
                    paras['ErrorInfo'] = 'sql execute error'
                else:
                    try:
                        return_value['Times'] = cursor.fetchone()[0]
                    except:
                        return_value['Times'] = 0
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 3
                paras['ErrorInfo'] = 'Openid acquisition error'
            return_value['Statue'] = paras['Statue']
            if return_value['Statue'] == 0:
                return_value['ErrorCode'] = paras['ErrorCode']
                return_value['ErrorInfo'] = paras['ErrorInfo']
            return_json = json.dumps(return_value)
            return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/user_views/get_advertise_times.html')


# 向服务器上存储用户信息
@csrf_exempt
def update_user_info(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Code', 'Sid', 'Auth', 'Password', 'Email', 'Dormitory', 'Type'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            open_id = get_code(paras['Code'])
            # open_id = paras['Code']
            if open_id is not None:
                sql = 'call SaveUserInfo(%s, %s, %s, %s, %s, %s, %s)'
                try:
                    cursor.execute(sql, (open_id, paras['Sid'], paras['Auth'], paras['Password'],
                                         paras['Email'], paras['Dormitory'], paras['Type']))
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 2
                    paras['ErrorInfo'] = 'Sql execute error'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/user_views/update_user_info.html')


# 在服务器上查询用户信息
@csrf_exempt
def select_user_info(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Code'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            open_id = get_code(paras['Code'])
            # open_id = paras['Code']
            if open_id is not None:
                sql1 = 'select S.Sid, Auth, Password, Mail, Dormitory, Type, Authority, UserName ' \
                       'from Subscribe S JOIN Authorization A1 on S.Sid = A1.Sid join UserInfo UI on A1.Sid = UI.Sid ' \
                       'where S.Openid = %s'
                try:
                    cursor.execute(sql1, (open_id,))
                except:
                    connection.rollback()
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 2
                    paras['ErrorInfo'] = 'Sql execute error'
                else:
                    result = cursor.fetchone()
                    if result is not None:
                        return_value['Sid'] = result[0]
                        return_value['Auth'] = result[1]
                        return_value['Password'] = result[2]
                        return_value['Email'] = result[3]
                        return_value['Dormitory'] = result[4]
                        return_value['Type'] = result[5]
                        return_value['Authority'] = result[6]
                        return_value['UserName'] = result[7]
                    else:
                        paras['Statue'] = 0
                        paras['ErrorCode'] = 3
                        paras['ErrorInfo'] = 'No user data'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/user_views/select_user_info.html')


# 在服务器上删除用户信息
@csrf_exempt
def delete_user_info(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Code'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            open_id = get_code(paras['Code'])
            # open_id = paras['Code']
            if open_id is not None:
                sql1 = 'call Userinfo_delete(%s)'
                try:
                    cursor.execute(sql1, (open_id,))
                except:
                    connection.rollback()
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 2
                    paras['ErrorInfo'] = 'Sql execute error'
                else:
                    connection.commit()
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/user_views/delete_user_info.html')
