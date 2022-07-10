import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json, connect_db, get_code


# 增加数据备份到云事件
@csrf_exempt
def push_custom_event(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Code', 'Events'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            openid = get_code(paras['Code'])
            # openid = paras['Code']
            try:
                sql_delete = "delete from CustomEvent where Openid = %s"
                cursor.execute(sql_delete, (openid,))
                for arr in paras['Events']:
                    sql_insert = "insert into CustomEvent(CEcode, CEname, PeriodFormat, " \
                                 "TeachingWeekFormat, WeekdayFormat, Content, Openid) " \
                                 "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql_insert, (arr['CEcode'], arr['CEname'], arr['PeriodFormat'],
                                                arr['TeachingWeekFormat'], arr['WeekdayFormat'], arr['Content'],
                                                openid))
                connection.commit()
            except Exception as e:
                connection.rollback()
                print(e)
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'sql execute error'

        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/course_table_views/push_custom_event.html')


# 增加数据同步到本地事件
@csrf_exempt
def pull_custom_event(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Code'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            openid = get_code(paras['Code'])
            # openid = paras['Code']
            try:
                sql = 'select CEcode, CEname, PeriodFormat, TeachingWeekFormat, WeekdayFormat, Content ' \
                      'from CustomEvent where Openid = %s'
                cursor.execute(sql, (openid,))
            except Exception as e:
                connection.rollback()
                print(e)
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'sql execute error'

            result = cursor.fetchall()
            event_array = []
            for event in result:
                event_dict = {
                    'CEcode': event[0],
                    'CEname': event[1],
                    'PeriodFormat': event[2],
                    'TeachingWeekFormat': event[3],
                    'WeekdayFormat': event[4],
                    'Content': event[5],
                }
                event_array.append(event_dict)

            return_value['Events'] = event_array

        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/course_table_views/pull_custom_event.html')
