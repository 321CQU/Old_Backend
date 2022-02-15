from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..tools import analysis_json, connect_db
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
                # 新旧学期交替之际，存在短暂的该接口无法获取到新学期信息的问题，因此让返回值直接返回空
                try:
                    res = session.get(f'https://my.cqu.edu.cn/api/resourceapi/session/info/{next_term_id}')
                    data = json.loads(res.content)['data']
                    return_value = {
                        'Term': data['year'] + data['term'],
                        'StartDate': data['beginDate'],
                        'EndDate': data['endDate']
                    }
                except:
                    return_value = {}
        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/school_info_views/get_next_term.html')


# 根据课程名称或教师名称，模糊查询相关课程列表
@csrf_exempt
def get_course_list(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key'], ['CourseName', 'TeacherName'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            course_name = paras.get('CourseName')
            teacher_name = paras.get('TeacherName')
            if course_name:
                sql = "select distinct C.Cid, C.Cname from Course C where locate(%s, C.Cname)"
                cursor.execute(sql, (course_name,))
                courses = cursor.fetchall()
                return_value['Courses'] = courses
            elif teacher_name:
                sql = "select distinct T.Tname, C.Cid, C.Cname from Teaching Te " \
                      "join Teacher T on T.Tid = Te.Tid " \
                      "join Course C on C.Cid = Te.Cid where locate(%s, T.Tname)"
                cursor.execute(sql, (teacher_name,))
                courses = cursor.fetchall()
                return_value['Courses'] = courses
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 1
                paras['ErrorInfo'] = 'Uncorrected Arguments'

        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/school_info_views/get_course_list.html')


# 根据课程编号(Cid)查询对应课程所有教师相关信息
@csrf_exempt
def get_course_detail(request):
    if request.method == 'POST' and request.body:
        post_json = request.body.decode('utf-8')
        post = json.loads(post_json)
        paras = analysis_json(post, ['Key', 'Cid'])
        connection, cursor = connect_db()
        return_value = {}
        if paras['Statue'] == 1:
            sql1 = "select distinct S.Term from Course C join Score S on C.Cid = S.Cid where C.Cid = %s"
            cursor.execute(sql1, (paras['Cid'],))
            terms = cursor.fetchall()
            temp = {}
            if len(terms):
                for term in terms:
                    # 该sql会判断该课程是否为等级制（成绩当中有中文且超过了总成绩数量的一半即为等级制），并分别返回相关信息，分数制有11列，等级制为8列
                    sql2 = "call CourseDetail(%s, %s)"
                    cursor.execute(sql2, (paras['Cid'], term[0]))
                    infos = cursor.fetchall()
                    temp[term[0]] = infos

                temp_dict = {}
                for term in terms:
                    if len(temp[term[0]][0]) == 11:
                        temp_dict[term[0]] = 0
                    else:
                        temp_dict[term[0]] = 1

                return_value['IsHierarchy'] = temp_dict

                return_value['CourseScore'] = temp
            else:
                paras['Statue'] = 0
                paras['ErrorCode'] = 2
                paras['ErrorInfo'] = 'There is no data related to this course'

        return_value['Statue'] = paras['Statue']
        if return_value['Statue'] == 0:
            return_value['ErrorCode'] = paras['ErrorCode']
            return_value['ErrorInfo'] = paras['ErrorInfo']
        return_json = json.dumps(return_value)
        return HttpResponse(return_json, content_type='application/json')
    elif request.method == 'GET':
        return render(request, '321CQU/school_info_views/get_course_detail.html')
