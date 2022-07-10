import datetime
from typing import Dict, List

from CQU321.register.WebsiteExpection import UserNotFound, NoAuthority
from CQU321.tools import has_authority
from CQU321.utils.ExceptionProcessor import process_exception, Result
from CQU321.utils.tools import *
from CQU321.utils.SqlProcessor import SqlProcessor


__all__ = ['send_post_process', 'update_post_process', 'get_post_list_process', 'get_post_detail_process',
           'send_reply_process', 'get_reply_process', 'delete_reply_process']


def send_post_v_1_0(params: Dict):
    process = SqlProcessor()
    now = datetime.datetime.now()
    now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    sql = "insert into Posts(Title, Content, Type, Author, UpdateDate) VALUES (%s, %s, %s, %s, %s)"
    process.execute(sql, (params['Title'], params['Content'], params['Type'], params['Author'], now_str))


def send_post_v_2_0(params: Dict):
    process = SqlProcessor()
    now = datetime.datetime.now()
    now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    sql = "insert into Posts(Title, Content, Type, Author, UpdateDate, IsAnonymous) VALUES (%s, %s, %s, %s, %s, %s)"
    process.execute(sql, (params['Title'], params['Content'], params['Type'], params['Author'], now_str,
                          params['IsAnonymous']))


@process_exception
def send_post_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': send_post_v_1_0,
        '2.0': send_post_v_2_0,
    }, params)

    result = func(params)

    return {
        'Version': params.pop('Version')
    }


def update_post_v_1_0(params: Dict):
    process = SqlProcessor()
    now = datetime.datetime.now()
    now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    if has_authority(params['Sid'], params['Pid'], 'delete' if params['IsDelete'] else 'update'):
        if params['IsDelete']:
            sql3 = "delete from Reply where Pid = %s"
            process.execute(sql3, (params['Pid'],))
            sql2 = "delete from Posts where Pid = %s"
            process.execute(sql2, (params['Pid'],))
        else:
            sql = "update Posts set Title = %s, Content = %s, UpdateDate = %s where Pid = %s"
            process.execute(sql, (params['Title'], params['Content'], now_str, params['Pid']))
    else:
        raise NoAuthority


def update_post_v_2_0(params: Dict):
    process = SqlProcessor()
    now = datetime.datetime.now()
    now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    if has_authority(params['Sid'], params['Pid'], 'delete' if params['IsDelete'] else 'update'):
        if params['IsDelete']:
            sql3 = "delete from Reply where Pid = %s"
            process.execute(sql3, (params['Pid'],))
            sql2 = "delete from Posts where Pid = %s"
            process.execute(sql2, (params['Pid'],))
        else:
            sql = "update Posts set Title = %s, Content = %s, UpdateDate = %s, IsAnonymous = %s where Pid = %s"
            process.execute(sql, (params['Title'], params['Content'], now_str, params['IsAnonymous'], params['Pid']))
    else:
        raise NoAuthority


@process_exception
def update_post_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': update_post_v_1_0,
        '2.0': update_post_v_2_0,
    }, params)

    result = func(params)

    return {
        'Version': params.pop('Version')
    }


def get_post_list_v_1_0(params: Dict):
    process = SqlProcessor()
    if params.get('Limit') is None:
        params['Limit'] = '50'
    if params['Type'] == 'all':
        sql = "select P.Pid, P.Title, substring(P.Content, 1, 50), P.Author, P.Type, " \
              "UI.UserName, UI.UserImg, P.UpdateDate, COUNT(R.Rid), Authority " \
              "from Posts P left join UserInfo UI on UI.Sid = P.Author " \
              "left join Reply R on P.Pid = R.Pid where P.Type != 'FK' group by P.Pid, P.UpdateDate " \
              f"order by UpdateDate desc limit {params['Limit']}"
        process.execute(sql)
    else:
        sql = "select P.Pid, P.Title, substring(P.Content, 1, 50), P.Author, Type, " \
              "UI.UserName, UI.UserImg, P.UpdateDate,  count(R.Rid), Authority " \
              "from Posts P left join UserInfo UI on UI.Sid = P.Author " \
              "left join Reply R on P.Pid = R.Pid where P.Type = %s group by P.Pid, P.UpdateDate " \
              f"order by UpdateDate desc limit {params['Limit']}"
        process.execute(sql, (params['Type'],))

    post_list = []
    for post in process.fetchall():
        post_dict = {
            'Pid': post[0],
            'Title': post[1],
            'Content': post[2],
            'Author': post[3],
            'Type': post[4],
            'UserName': post[5],
            'UserImg': post[6],
            'UpdateDate': str(post[7]),
            'ReplyNum': post[8],
            'Authority': post[9],
        }
        post_list.append(post_dict)

    return post_list


def get_post_list_v_2_0(params: Dict):
    process = SqlProcessor()
    if params['Type'] == 'all':
        sql = "select P.Pid, P.Title, substring(P.Content, 1, 50), P.Author, P.Type, " \
              "UI.UserName, UI.UserImg, P.UpdateDate, COUNT(R.Rid), Authority, P.IsAnonymous " \
              "from Posts P left join UserInfo UI on UI.Sid = P.Author " \
              "left join Reply R on P.Pid = R.Pid where P.Type != 'FK' group by P.Pid, P.UpdateDate " \
              f"order by UpdateDate desc limit %s, %s"
        process.execute(sql, (20 * params['Page'], 20 * params['Page'] + 20))
    else:
        sql = "select P.Pid, P.Title, substring(P.Content, 1, 50), P.Author, Type, " \
              "UI.UserName, UI.UserImg, P.UpdateDate,  count(R.Rid), Authority, P.IsAnonymous " \
              "from Posts P left join UserInfo UI on UI.Sid = P.Author " \
              "left join Reply R on P.Pid = R.Pid where P.Type = %s group by P.Pid, P.UpdateDate " \
              f"order by UpdateDate desc limit %s, %s"
        process.execute(sql, (params['Type'], 20 * params['Page'], 20 * params['Page'] + 20))

    post_list = []
    for post in process.fetchall():
        post_dict = {
            'Pid': post[0],
            'Title': post[1],
            'Content': post[2],
            'Author': post[3],
            'Type': post[4],
            'UserName': post[5],
            'UserImg': post[6],
            'UpdateDate': str(post[7]),
            'ReplyNum': post[8],
            'Authority': post[9],
            'IsAnonymous': bool(post[10]),
        }
        post_list.append(post_dict)

    return post_list


@process_exception
def get_post_list_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': get_post_list_v_1_0,
        '2.0': get_post_list_v_2_0,
    }, params)

    result = func(params)

    return {
        'PostList': result,
        'Version': params.pop('Version')
    }


def get_post_detail_v_1_0(params: Dict):
    process = SqlProcessor()
    sql = "select Pid, Title, Content, Author, Type, UserName, UserImg, UpdateDate, Authority " \
          "from Posts P left join UserInfo UI on UI.Sid = P.Author " \
          "where Pid = %s"
    process.execute(sql, params['Pid'])
    detail = process.fetchone()
    if detail is not None:
        post_detail = {
            'Pid': detail[0],
            'Title': detail[1],
            'Content': detail[2],
            'Author': detail[3],
            'Type': detail[4],
            'UserName': detail[5],
            'UserImg': detail[6],
            'UpdateDate': str(detail[7]),
            'Authority': detail[8],
        }
        return post_detail
    else:
        raise UserNotFound


def get_post_detail_v_2_0(params: Dict):
    process = SqlProcessor()
    sql = "select Title, Content, Author, Type, UserName, UserImg, UpdateDate, Authority, IsAnonymous " \
          "from Posts P left join UserInfo UI on UI.Sid = P.Author " \
          "where Pid = %s"
    process.execute(sql, params['Pid'])
    detail = process.fetchone()
    if detail is not None:
        post_detail = {
            'Title': detail[0],
            'Content': detail[1],
            'Author': detail[2],
            'Type': detail[3],
            'UserName': detail[4],
            'UserImg': detail[5],
            'UpdateDate': str(detail[6]),
            'Authority': detail[7],
            'IsAnonymous': bool(detail[8]),
        }
        return post_detail
    else:
        raise UserNotFound


@process_exception
def get_post_detail_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': get_post_detail_v_1_0,
        '2.0': get_post_detail_v_2_0,
    }, params)

    result = func(params)

    return {
        'PostDetail': result,
        'Version': params.pop('Version')
    }


def send_reply_v_1_0(params: Dict):
    process = SqlProcessor()
    now = datetime.datetime.now()
    now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    sql = "insert into Reply (Content, Author, UpdateTime, Pid) VALUES (%s, %s, %s, %s)"
    process.execute(sql, (params['Content'], params['Author'], now_str, params['Pid']))


def send_reply_v_2_0(params: Dict):
    process = SqlProcessor()
    now = datetime.datetime.now()
    now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    sql = "insert into Reply (Content, Author, UpdateTime, Pid, IsAnonymous) VALUES (%s, %s, %s, %s, %s)"
    process.execute(sql, (params['Content'], params['Author'], now_str, params['Pid'], params['IsAnonymous']))


@process_exception
def send_reply_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': send_reply_v_1_0,
        '2.0': send_reply_v_2_0,
    }, params)

    result = func(params)

    return {
        'Version': params.pop('Version')
    }


def get_reply_v_1_0(params: Dict):
    process = SqlProcessor()
    if params.get('Limit') is None:
        sql = "select Rid, Content, Author, UpdateTime, UserName, UserImg, Authority from " \
              "Reply R left join UserInfo UI on R.Author = UI.Sid where Pid = %s order by UpdateTime desc"
    else:
        sql = "select Rid, Content, Author, UpdateTime, UserName, UserImg, Authority from " \
              "Reply R left join UserInfo UI on R.Author = UI.Sid where Pid = %s " \
              f"limit {params['Limit']} order by UpdateTime desc"
    process.execute(sql, params['Pid'])

    replies = []
    for reply in process.fetchall():
        temp = {
            'Rid': reply[0],
            'Content': reply[1],
            'Author': reply[2],
            'UpdateTime': str(reply[3]),
            'UserName': reply[4],
            'UserImg': reply[5],
            'Authority': reply[6],
        }
        replies.append(temp)

    return replies


def get_reply_v_2_0(params: Dict):
    process = SqlProcessor()

    sql = "select Rid, Content, Author, UpdateTime, UserName, UserImg, Authority, IsAnonymous from " \
          "Reply R left join UserInfo UI on R.Author = UI.Sid where Pid = %s " \
          "order by UpdateTime limit %s, %s"
    process.execute(sql, (params['Pid'], 10 * params['Page'], 10 * params['Page'] + 10))

    replies = []
    for reply in process.fetchall():
        temp = {
            'Rid': reply[0],
            'Content': reply[1],
            'Author': reply[2],
            'UpdateTime': str(reply[3]),
            'UserName': reply[4],
            'UserImg': reply[5],
            'Authority': reply[6],
            'IsAnonymous': bool(reply[7]),
        }
        replies.append(temp)

    return replies


@process_exception
def get_reply_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': get_reply_v_1_0,
        '2.0': get_reply_v_2_0,
    }, params)

    result = func(params)

    return {
        'Reply': result,
        'Version': params.pop('Version')
    }


def delete_reply_v_1_0(params: Dict):
    process = SqlProcessor()
    if has_authority(params['Sid'], params['Rid'], "delete reply"):
        sql = "delete from Reply where Rid = %s"
        process.execute(sql, (params['Rid'],))
    else:
        raise NoAuthority


@process_exception
def delete_reply_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': delete_reply_v_1_0,
    }, params)

    result = func(params)

    return {
        'Version': params.pop('Version')
    }

