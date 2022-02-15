import mycqu.score
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..CQUGetter import CQUGetter
from ..tools import analysis_json, get_code, connect_db

import json
import re


# 通过学号查询学生姓名
@csrf_exempt
def student_validation(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid'])
        connection, cursor = connect_db()
        res = re.match(r'[\u4E00-\u9FA5]+', paras['Sid'])
        return_value = {}
        if res is not None:
            paras['Statue'] = 0
            paras['ErrorCode'] = 2
            paras['ErrorInfo'] = 'Uncorrected Sid'
        if paras['Statue'] == 1:
            sql = 'SELECT Sid, Sname FROM Student where Sid = %s'
            cursor.execute(sql, (paras['Sid'],))
            result = cursor.fetchone()
            if result is not None:
                return_value['Sid'] = result[0]
                return_value['Sname'] = result[1]
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 3
                paras['ErrorInfo'] = 'There is no information about this student in the database'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/student_views/stuVal.html')


# 查询学生总志愿时长
@csrf_exempt
def total_duration(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            sql = 'select Sid, SUM(Duration) from VolunteerActivity where Sid = %s group by Sid'
            cursor.execute(sql, (paras['Sid'],))
            result = cursor.fetchone()
            if result is not None:
                return_value['Sid'] = result[0]
                return_value['TotalDuration'] = float(result[1])
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'There is no information about this student in the database'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/student_views/total_duration.html')


# 查询学生所有志愿活动相关信息
@csrf_exempt
def all_activity(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            sql = 'SELECT FI.StartDate, FI.EndDate, AI.Aname, VA.Duration, AI.Fid ' \
                  'FROM VolunteerActivity VA join ActivityInfo AI on VA.Aid = AI.Aid ' \
                  'join FileInfo FI on AI.Fid = FI.Fid ' \
                  'where VA.Sid = %s order by StartDate desc'
            cursor.execute(sql, (paras['Sid'],))
            result = cursor.fetchall()
            if result is not None:
                temp = []
                for r in result:
                    r = list(r)
                    r[0] = str(r[0])
                    r[1] = str(r[1])
                    r[3] = float(r[3])
                    temp.append(r)
                return_value['AllActivity'] = temp
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'There is no information about this student in the database'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/student_views/all_activity.html')


# 查询学生成绩
@csrf_exempt
def get_score(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'UserName', 'Password', 'Code', 'NeedAll'], ['Debug'])
        connection, cursor = connect_db()
        return_value = {}
        res = re.match(r'[\u4E00-\u9FA5]+', paras['Sid'])
        if res is not None:
            paras['Statue'] = 0
            paras['ErrorCode'] = 2
            paras['ErrorInfo'] = 'Uncorrected Sid'
        if paras['Statue'] == 1:
            getter = CQUGetter(sid=paras['Sid'])
            if getter.is_match(paras['UserName'], paras['Password']):
                open_id = get_code(paras['Code'])
                if open_id is not None:
                    try:
                        score_log = getter.get_score(connection, cursor, open_id, paras['NeedAll'])
                    except mycqu.score.CQUWebsiteError:
                        paras['Statue'] = 0
                        paras['ErrorCode'] = 6
                        paras['ErrorInfo'] = 'CQU website statue error, please try again later'
                    else:
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
        return render(request, '321CQU/student_views/get_score.html')


# 查询考试安排
@csrf_exempt
def get_exam(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'UserName', 'Password'])
        connection, cursor = connect_db()
        res = re.match(r'[\u4E00-\u9FA5]+', paras['Sid'])
        if res is not None:
            paras['Statue'] = 0
            paras['ErrorCode'] = 2
            paras['ErrorInfo'] = 'Uncorrected Sid'
        return_value = {}
        if paras['Statue'] == 1:
            getter = CQUGetter(sid=paras['Sid'], use_selenium=False)
            if getter.is_match(paras['UserName'], paras['Password']):
                exam_log = getter.get_exam()
                if exam_log is not None:
                    return_value['Exams'] = exam_log
                else:
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 3
                    paras['ErrorInfo'] = 'There is no exam information about this student'
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 4
                paras['ErrorInfo'] = 'Account password unmatch'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/student_views/get_exam.html')


# 获取课表
@csrf_exempt
def get_course(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'UserName', 'Password'])
        res = re.match(r'[\u4E00-\u9FA5]+', paras['Sid'])
        if res is not None:
            paras['Statue'] = 0
            paras['ErrorCode'] = 2
            paras['ErrorInfo'] = 'Uncorrected Sid'
        return_value = {}
        if paras['Statue'] == 1:
            getter = CQUGetter(sid=paras['Sid'], use_selenium=False)
            if getter.is_match(paras['UserName'], paras['Password']):
                course_log = getter.get_courses()
                if course_log is not None and len(course_log):
                    return_value['Courses'] = course_log
                else:
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 3
                    paras['ErrorInfo'] = 'There is no courses information about this student'
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 4
                paras['ErrorInfo'] = 'Account password unmatch'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/student_views/get_course.html')


# 获取学生选课信息
@csrf_exempt
def get_enrollment(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Sid', 'UserName', 'Password'])
        res = re.match(r'[\u4E00-\u9FA5]+', paras['Sid'])
        if res is not None:
            paras['Statue'] = 0
            paras['ErrorCode'] = 2
            paras['ErrorInfo'] = 'Uncorrected Sid'
        return_value = {}
        if paras['Statue'] == 1:
            getter = CQUGetter(sid=paras['Sid'], use_selenium=False)
            if getter.is_match(paras['UserName'], paras['Password']):
                course_log = getter.get_enrollment()
                if course_log is not None and len(course_log):
                    return_value['Courses'] = course_log
                else:
                    paras['Statue'] = 0
                    paras['ErrorCode'] = 3
                    paras['ErrorInfo'] = 'There is no enrolled courses information about this student'
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 4
                paras['ErrorInfo'] = 'Account password unmatch'
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    else:
        return render(request, '321CQU/student_views/get_enrollment.html')
