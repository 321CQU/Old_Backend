from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json, get_code, connect_db
from ..CQUGetter import CQUGetter

import json
import hashlib


@csrf_exempt
def message_validation(request):
    if request.method == 'GET':
        with open('./WXlog.json') as f:
            f.write('{}')
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        token = '*******'  # 这里填在微信小程序端设置的token

        temp_arr = [timestamp, nonce, token]
        temp_arr.sort()
        temp_str = ''.join(temp_arr)
        temp = hashlib.sha1(temp_str.encode("utf-8")).hexdigest()
        if temp == signature:
            return HttpResponse(echostr)
    else:
        mess_json = request.body.decode('utf-8')
        post = json.loads(mess_json)
        with open('./WXlog.json') as f:
            f.write(mess_json)
        post['Key'] = 'CQUz5321'
        try:
            paras = analysis_json(post, ['Key', 'FromUserName', 'Event'])
            connection, cursor = connect_db()
            if (paras['Event'] == 'subscribe_msg_popup_event' or paras['Event'] == 'subscribe_msg_change_event') and paras['Statue'] == 1:
                sub_list = post['List']
                template_id = sub_list['TemplateId']
                statue = sub_list['SubscribeStatusString']
                # TODO:增加template_id校验
                if statue == 'accept':
                    sql = 'call WXSubscribe(%s, 1)'
                elif statue == 'reject':
                    sql = 'call WXSubscribe(%s, 0)'
                try:
                    cursor.execute(sql, (paras['FromUserName'],))
                except:
                    connection.rollback()
                else:
                    connection.commit()
                    return HttpResponse('success')
            elif paras['Event'] == 'subscribe_msg_sent_event' and paras['Statue'] == 1:
                return HttpResponse('success')
        except Exception as e:
            print(e)


# 因为微信提供的订阅消息推送很奇怪，而且我们小程序的订阅功能需要获取用户账号密码，这里就给了一个单独的接口
@csrf_exempt
def subscribe_message(request):
    if request.method == 'POST':
        return_value = {}
        sub_json = request.body.decode('utf-8')
        post = json.loads(sub_json)
        paras = analysis_json(post, ['Key', 'Code', 'Sid', 'UserName', 'Password'])
        connection, cursor = connect_db()
        if paras['Statue'] == 1:
            getter = CQUGetter()
            open_id = get_code(paras['Code'])
            if open_id is not None:
                if getter.is_match(paras['UserName'], paras['Password']):
                    sql1 = 'call MySubscribe(%s, %s)'
                    sql2 = 'call AuthAdd(%s, %s, %s)'
                    sql3 = 'call WXSubscribe(%s, 1)'
                    try:
                        cursor.execute(sql1, (open_id, paras['Sid']))
                        cursor.execute(sql2, (paras['Sid'], paras['UserName'], paras['Password']))
                        cursor.execute(sql3, (open_id, ))
                    except:
                        connection.rollback()
                        paras['Statue'] = 0
                        paras['ErrorCode'] = 2
                        paras['ErrorInfo'] = 'Sql execute error'
                    else:
                        connection.commit()
                else:
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 3
                    paras['ErrorInfo'] = 'Account password unmatch'
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 4
                paras['ErrorInfo'] = 'Openid acquisition error'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/message_views/subscribe.html')
