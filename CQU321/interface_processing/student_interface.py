from typing import Dict, List

from CQU321.register.WebsiteExpection import InfoIsNull
from CQU321.utils.ExceptionProcessor import process_exception, Result
from CQU321.utils.SqlProcessor import _connect_db
from CQU321.utils.tools import *
from CQU321.utils.tools import parse_dict

from CQUGetter.Getter.DeanGetter import DeanGetter

__all__ = ("get_course_process", "get_enrollment_process", "get_gpa_ranking_process", "get_score_process")


def _launch_room_name(courses: List[Dict]):
    for course in courses:
        if course.get('RoomName'):
            position = course.pop('RoomPosition')
            course['RoomName'] = course['RoomName'] + (('-' + position) if position else '')
        else:
            course.pop('RoomPosition')


def _get_course_v_1_0(getter: DeanGetter, params: Dict) -> List[Dict]:
    result = _get_course_v_2_0(getter, params)
    result, _ = parse_dict(result, name_change={
        'WeekDay': 'WeekDayFormat',
        'CourseNum': 'ClassNbr',
        'Period': 'PeriodFormat',
        'Weeks': 'TeachingWeekFormat',
    })

    return result


@invalid_login_cookie_process
def _get_course_v_2_0(getter: DeanGetter, params: Dict) -> List[Dict]:
    getter_login_and_access(getter, params)
    result = getter.get_course_by_mycqu(params['Sid'])

    return result


@process_exception
def get_course_process(params: Result) -> Dict:
    params = params.get_data()

    func = func_select_by_version({
        '1.0': _get_course_v_1_0,
        '2.0': _get_course_v_2_0,
    }, params)
    courses = func(DeanGetter(), params)

    if len(courses) == 0:
        raise InfoIsNull

    _launch_room_name(courses)

    return {
        'Courses': courses,
        'Version': params.pop('Version')
    }


def _get_enrollment_v_1_0(getter: DeanGetter, params: Dict) -> List[Dict]:
    result = _get_enrollment_v_2_0(getter, params)
    result, _ = parse_dict(result, name_change={
        'WeekDay': 'WeekDayFormat',
        'CourseNum': 'ClassNbr',
        'Period': 'PeriodFormat',
        'Weeks': 'TeachingWeekFormat',
    })

    return result


@invalid_login_cookie_process
def _get_enrollment_v_2_0(getter: DeanGetter, params: Dict) -> List[Dict]:
    getter_login_and_access(getter, params)
    result = getter.get_enrollment(params['Sid'])

    return result


@process_exception
def get_enrollment_process(params: Result) -> Dict:
    params = params.get_data()

    func = func_select_by_version({
        '1.0': _get_enrollment_v_1_0,
        '2.0': _get_enrollment_v_2_0,
    }, params)

    # TODO: 处理该函数在高并发情况下可能报错的异常
    try:
        enrollments = func(DeanGetter(), params)
    except Exception as e:
        enrollments = []

    _launch_room_name(enrollments)

    return {
        'Courses': enrollments,
        'Version': params.pop('Version')
    }


@invalid_login_cookie_process
def _get_gpa_ranking_v_2_0(getter: DeanGetter, params: Dict) -> Dict:
    getter_login_and_access(getter, params)

    result = getter.get_gpa_ranking()

    return result


def _get_gpa_ranking_v_1_0(getter: DeanGetter, params: Dict) -> Dict:
    result = _get_gpa_ranking_v_2_0(getter, params)

    result['gpa'] = str(result.pop('GPA'))
    result['majorRanking'] = str(result.pop('MajorRank'))
    result['gradeRanking'] = str(result.pop('GradeRank'))
    result['classRanking'] = str(result.pop('ClassRank'))

    return result


@process_exception
def get_gpa_ranking_process(params: Result) -> Dict:
    params = params.get_data()

    func = func_select_by_version({
        '1.0': _get_gpa_ranking_v_1_0,
        '2.0': _get_gpa_ranking_v_2_0
    }, params)

    result = func(DeanGetter(), params)

    return {
        'GpaRanking': result,
        'Version': params.pop('Version')
    }


@sql_exception_process
def add_score_to_database(code, scores: List[Dict], is_debug: bool):
    openid = get_code(code, is_debug)
    connection, cursor = _connect_db()

    for score in scores:
        sql = "call insertScore(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            openid, score['CourseName'], score['CourseCode'], float(score['Credit']),
            score['Score'], score['InstructorName'], score['StudyNature'],
            score['CourseNature'], score['Term']))
        connection.commit()


@invalid_login_cookie_process
def _get_score_v_2_0(getter: DeanGetter, params: Dict) -> Dict:
    getter_login_and_access(getter, params)
    score = getter.get_score_by_mycqu()
    minor_score = getter.get_minor_score_by_mycqu()

    add_score_to_database(params.get('Code'), score, params.get('Debug'))
    add_score_to_database(params.get('Code'), minor_score, params.get('Debug'))
    score, _ = parse_dict(score, need_pop=['CourseNature'], move_as_key='Term')
    minor_score, _ = parse_dict(minor_score, need_pop=['CourseNature'], move_as_key='Term')

    return {
        '主修': score,
        '辅修': minor_score
    }


@invalid_login_cookie_process
def _get_score_v_1_0(getter: DeanGetter, params: Dict) -> Dict:
    getter_login_and_access(getter, params)
    result = getter.get_score_by_mycqu()
    result.extend(getter.get_minor_score_by_mycqu())
    add_score_to_database(params.get('Code'), result, params.get('Debug'))

    result, _ = parse_dict(result, name_change={
        'Score': 'EffectiveScoreShow',
        'Credit': 'CourseCredit'
    }, move_as_key='Term')

    return result


@process_exception
def get_score_process(params: Result) -> Dict:
    params = params.get_data()

    if params.get('Debug') is None:
        params['Debug'] = False

    func = func_select_by_version({
        '1.0': _get_score_v_1_0,
        '2.0': _get_score_v_2_0,
    }, params)

    result = func(DeanGetter(), params)

    return {
        'ScoreLog': result,
        'Version': params.pop('Version')
    }
