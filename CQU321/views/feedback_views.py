from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json, connect_db

import json
import datetime


# 发送小程序反馈
@csrf_exempt
def send_feedback(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'Content'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            now = datetime.datetime.now()
            now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
            sql = 'insert into Feedback(sid, content, ftime) values (%s, %s, %s)'
            try:
                cursor.execute(sql, (paras['Sid'], paras['Content'], now_str))
                connection.commit()
                return_value['Statue'] = 1
            except:
                connection.rollback()
                return_value['Statue'] = 0
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/feedback_views/send_feedback.html')


# 查询小程序反馈
@csrf_exempt
def get_feedback(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key'], ['Limit'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            if paras['Limit'] is not None:
                limit = paras['Limit']
                if ',' in str(limit):
                    limit = limit.split(',')
                    sql = 'select F.FBid, F.Sid, UI.UserName, UI.UserImg, F.Content, F.Ftime, count(C.Comid) from Feedback F ' \
                          'left join Comment C on F.FBid = C.FBid ' \
                          'left join UserInfo UI on F.Sid = UI.Sid group by F.FBid, F.Ftime order by F.Ftime desc ' \
                          'limit %s, %s'
                    cursor.execute(sql, (int(limit[0]), int(limit[1])))
                else:
                    sql = 'select F.FBid, F.Sid, UI.UserName, UI.UserImg, F.Content, F.Ftime, count(C.Comid) from Feedback F ' \
                          'left join Comment C on F.FBid = C.FBid ' \
                          'left join UserInfo UI on F.Sid = UI.Sid group by F.FBid, F.Ftime order by F.Ftime desc ' \
                          'limit %s'
                    cursor.execute(sql, (int(limit),))
            else:
                sql = 'select F.FBid, F.Sid, UI.UserName, UI.UserImg, F.Content, F.Ftime, count(C.Comid) from Feedback F ' \
                          'left join Comment C on F.FBid = C.FBid ' \
                          'left join UserInfo UI on F.Sid = UI.Sid group by F.FBid, F.Ftime order by F.Ftime desc'
                cursor.execute(sql)

            result = cursor.fetchall()
            temp = []
            for t in result:
                temp_dict = {
                    'FBid': t[0],
                    'Sid': t[1],
                    'UserName': t[2],
                    'UserImg': t[3],
                    'Content': t[4],
                    'Time': str(t[5]),
                    'CommentNum': t[6]
                }
                temp.append(temp_dict)
            return_value['Statue'] = 1
            return_value['FeedbackList'] = temp
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/feedback_views/get_feedback.html')


# 发送小程序评论
@csrf_exempt
def send_comment(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'Content', 'FBid'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            now = datetime.datetime.now()
            now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
            sql = 'insert into Comment (FBid, Sid, Content, Ctime) VALUES (%s, %s, %s, %s)'
            try:
                cursor.execute(sql, (paras['FBid'], paras['Sid'], paras['Content'], now_str))
                connection.commit()
            except:
                connection.rollback()
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'sql execute error'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/feedback_views/send_comment.html')


# 获取小程序评论
@csrf_exempt
def get_comment(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'FBid'], ['Limit'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            if paras['Limit'] is not None:
                limit = paras['Limit']
                if ',' in str(limit):
                    limit = limit.split(',')
                    sql = 'select C.Sid, UI.UserName, UI.UserImg, C.Content, C.Ctime ' \
                          'from Comment C join UserInfo UI on C.Sid = UI.Sid where C.FBid = %s order by Ctime desc ' \
                          'limit %s, %s'
                    cursor.execute(sql, (paras['FBid'], int(limit[0]), int(limit[1])))
                else:
                    sql = 'select C.Sid, UI.UserName, UI.UserImg, C.Content, C.Ctime ' \
                          'from Comment C join UserInfo UI on C.Sid = UI.Sid where C.FBid = %s order by Ctime desc ' \
                          'limit %s'
                    cursor.execute(sql, (paras['FBid'], int(limit),))
            else:
                sql = 'select C.Sid, UI.UserName, UI.UserImg, C.Content, C.Ctime ' \
                      'from Comment C join UserInfo UI on C.Sid = UI.Sid where C.FBid = %s order by Ctime desc'
                cursor.execute(sql, (paras['FBid'],))

            result = cursor.fetchall()
            temp = []
            for t in result:
                temp_dict = {
                    'Sid': t[0],
                    'UserName': t[1],
                    'UserImg': t[2],
                    'Content': t[3],
                    'Time': str(t[4])
                }
                temp.append(temp_dict)
            return_value['Statue'] = 1
            return_value['FeedbackList'] = temp
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/feedback_views/get_comment.html')
