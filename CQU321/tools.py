import pymysql
import requests
import json
import time
import fcntl
from configparser import ConfigParser
from Website.settings import BASE_DIR

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/321CQU_Config.ini')


def connect_db():
    connection = pymysql.connect(
        host=config.get('321CQU_Database', 'host'),
        port=config.getint('321CQU_Database', 'port'),
        user=config.get('321CQU_Database', 'user'),
        password=config.get('321CQU_Database', 'password'),
        database=config.get('321CQU_Database', 'database')
    )
    cursor = connection.cursor()
    return connection, cursor


def analysis_json(post, args, opt_paras=None):
    temp = {}
    try:
        for arg in args:
            temp[arg] = post[arg]
    except:
        temp['Statue'] = 0
        temp['ErrorCode'] = 1
        temp['ErrorInfo'] = 'Uncorrected Arguments'
    else:
        if temp['Key'] == config.get('Website', 'Key'):
            temp['Statue'] = 1
            if opt_paras is not None:
                for para in opt_paras:
                    if para in post:
                        temp[para] = post[para]
                    else:
                        temp[para] = None
        else:
            temp['Statue'] = 0
            temp['ErrorCode'] = 0
            temp['ErrorInfo'] = 'Uncorrected Key'
    return temp


def update_token(file_path=config.get('Website', 'WX_json_save_path')):
    try:
        with open(file_path + 'WX.json', 'r') as f:
            fcntl.lockf(f, fcntl.LOCK_SH)
            content = json.loads(f.read())
            last_time = content['timestamp']
            expires = content['expires_in']
            fcntl.lockf(f, fcntl.LOCK_UN)
    except:
        last_time = 0
        expires = 0

    if last_time + expires < int(time.time()):
        res = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential',
                           params={'appid': config.get('Weixin_App_Setting', 'appid'),
                                   'secret': config.get('Weixin_App_Setting', 'secret')})
        token = json.loads(res.content)
        token['timestamp'] = int(time.time())
        token_json = json.dumps(token)
        with open(file_path + 'WX.json', 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(token_json)
            fcntl.flock(f, fcntl.LOCK_UN)


def send_message(template_id, open_id, data, file_path=config.get('Website', 'WX_json_save_path')):
    if template_id == 0:
        template = config.get('Weixin_App_Setting', 'score_template')
        page = 'pages/center/grade/grade'
    else:
        template = config.get('Weixin_App_Setting', 'exam_template')
        page = 'pages/center/center'
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}'
    update_token(file_path)
    with open(file_path + 'WX.json', 'r') as f:
        fcntl.lockf(f, fcntl.LOCK_SH)
        access_token = json.loads(f.read())['access_token']
        fcntl.lockf(f, fcntl.LOCK_UN)
    message = {'touser': open_id, 'template_id': template, 'page': page, 'data': data}
    mess_json = json.dumps(message)
    res_json = requests.post(url.format(access_token), mess_json)
    res = json.loads(res_json.content)
    if res['errcode'] == 43101:
        sql = 'call WXSubscribe(%s, 0)'
        connection, cursor = connect_db()
        try:
            cursor.execute(sql, (open_id,))
        except:
            connection.rollback()
        else:
            connection.commit()


def launch_score_data(name, score):
    data = {'thing1': {'value': name}, 'thing2': {'value': score}}
    return data


def get_code(code):
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'
    res = requests.get(url.format(config.get('Weixin_App_Setting', 'appid'),
                                  config.get('Weixin_App_Setting', 'secret'),
                                  code))
    try:
        open_id = json.loads(res.content)['openid']
    except:
        with open('./code_get_error', 'ab') as f:
            f.write(res.content)
        open_id = None
    return open_id


def has_authority(sid, id, type):
    connection, cursor = connect_db()
    sql1 = "select Authority from UserInfo where Sid = %s"
    cursor.execute(sql1, (sid,))
    user_authority = cursor.fetchone()[0]
    if type == "delete reply":
        sql2 = "select R.Author, P.Type, P.Author from Reply R join Posts P on P.Pid = R.Pid where R.Author = %s"
    else:
        sql2 = "select Type, Author from Posts where Pid = %s"

    cursor.execute(sql2, (id,))
    post_info = cursor.fetchone()


    if type == 'delete reply':
        if user_authority == 'super' or user_authority == post_info[1] or sid == post_info[0] or sid == post_info[2]:
            return True
        else:
            return False
    else:
        if user_authority == "super" or user_authority == post_info[0] or sid == post_info[1]:
            return True
        else:
            return False


if __name__ == '__main__':
    code = '003YRoll2MBvr84myFkl2GvRjI0YRolF'
    print(get_code(code))
