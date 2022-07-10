from typing import Dict, List

from CQU321.utils.ExceptionProcessor import process_exception, Result
from CQU321.utils.tools import *
from CQU321.utils.SqlProcessor import SqlProcessor

from CQU321.register.WebsiteExpection import UserNotFound, IncorrectParams

from CQUWebsite.utils import read_activity_announcement

__all__ = ['get_announcement_detail_process', 'get_announcement_list_process', 'get_group_info_process',
           'subscribe_group_process', 'subscribe_list_process']


def analyse_announcement_list_data(announcements: List):
    result = []

    for data in announcements:
        temp = {
            'Aid': data[0],
            'Title': data[1],
            'Name': data[2],
            'CoverUrl': data[3],
            'StartDate': str(data[4]),
            'EndDate': str(data[5]),
            'UpdateDate': str(data[6]),
        }
        result.append(temp)

    return result


def get_announcement_list_v_2_0(params: Dict):
    process = SqlProcessor()
    process.execute('select Aid, Title, NickName, CoverUrl, StartDate, EndDate, UpdateDate'
                    ' from ActivityAnnouncement AA join `Group` U on AA.UserName = U.Username '
                    'where IsPublished = 1 group by UpdateDate desc limit %s, %s',
                    (20 * params['Page'], 20 * params['Page'] + 20))
    res = process.fetchall()

    return analyse_announcement_list_data(res)


def get_announcement_list_v_2_1(params: Dict):
    process = SqlProcessor()
    if params['Type'] == 'subscribe':
        sql = 'select Aid, Title, NickName, CoverUrl, StartDate, EndDate, UpdateDate ' \
              'from ActivityAnnouncement AA join `Group` U on AA.UserName = U.Username ' \
              'where IsPublished = 1 and ' \
              'U.Username in (select distinct GroupName from GroupFollower GF where GF.Sid = %s) ' \
              'group by UpdateDate desc limit %s, %s'
        process.execute(sql, (params['UserName'], 20 * params['Page'], 20 * params['Page'] + 20))
    elif params['Type'] == 'normal':
        sql = 'select Aid, Title, NickName, CoverUrl, StartDate, EndDate, UpdateDate ' \
              'from ActivityAnnouncement AA join `Group` U on AA.UserName = U.Username ' \
              'where IsPublished = 1 group by UpdateDate desc limit %s, %s'
        process.execute(sql, (20 * params['Page'], 20 * params['Page'] + 20))
    elif params['Type'] == 'group':
        sql = 'select Aid, Title, NickName, CoverUrl, StartDate, EndDate, UpdateDate ' \
              'from ActivityAnnouncement AA join `Group` U on AA.UserName = U.Username ' \
              'where U.Username in (select GroupName from GroupMember GM where GM.Sid = %s) ' \
              'group by UpdateDate desc limit %s, %s'
        process.execute(sql, (params['Sid'], 20 * params['Page'], 20 * params['Page'] + 20))
    else:
        raise IncorrectParams

    return analyse_announcement_list_data(process.fetchall())


@process_exception
def get_announcement_list_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': get_announcement_list_v_2_0,
        '2.1': get_announcement_list_v_2_1
    }, params)

    result = func(params)

    return {
        'Announcements': result,
        'Version': params.pop('Version')
    }


def get_announcement_detail_v_2_0(params: Dict):
    return read_activity_announcement(params['Id'])


@process_exception
def get_announcement_detail_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': get_announcement_detail_v_2_0
    }, params)

    result = func(params)

    return {
        'Markdown': result,
        'Version': params.pop('Version')
    }


def get_group_info_v_2_0(params: Dict):
    process = SqlProcessor()
    process.execute('select AvatarPath from `Group` where NickName = %s', (params['Name'],))
    res = process.fetchone()
    if res:
        return res[0]
    else:
        raise UserNotFound


@process_exception
def get_group_info_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': get_group_info_v_2_0
    }, params)

    result = func(params)

    return {
        'Avatar': result,
        'Version': params.pop('Version')
    }


def subscribe_group_v_2_0(params: Dict):
    process = SqlProcessor()
    if params['Type'] == 1:
        sql = "call subscribe_group(%s, %s)"
    elif params['Type'] == 0:
        sql = "delete from GroupFollower " \
              "where GroupName = (select distinct Username from `Group` where NickName = %s) and Sid = %s"
    else:
        raise IncorrectParams

    process.execute(sql, (params['GroupName'], params['Sid']))

    if params['Type'] == 1 and process.fetchone()[0] == 0:
        raise IncorrectParams


@process_exception
def subscribe_group_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': subscribe_group_v_2_0
    }, params)

    func(params)

    return {
        'Version': params.pop('Version')
    }


def subscribe_list_v_2_0(params: Dict):
    process = SqlProcessor()
    sql = 'select NickName from `Group` G join GroupFollower GF on G.Username = GF.GroupName where GF.Sid = %s'
    process.execute(sql, (params['Sid'],))

    result = []
    for data in process.fetchall():
        temp = {
            'GroupName': data[0]
        }
        result.append(temp)

    return result


@process_exception
def subscribe_list_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': subscribe_list_v_2_0
    }, params)

    result = func(params)

    return {
        'Version': params.pop('Version'),
        'Group': result
    }
