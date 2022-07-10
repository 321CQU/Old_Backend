import re
from typing import List, Dict, Any, Union, Optional
from mycqu.auth import login
from mycqu.mycqu import access_mycqu
from mycqu.exam import get_exam_raw
from mycqu.course import get_course_raw
from mycqu.score import get_score_raw, get_gpa_ranking_raw
from mycqu.card import get_fees_raw, get_card_raw, access_card, get_bill_raw
from mycqu.library import get_curr_books_raw, get_history_books_raw, access_library, BookInfo
from mycqu.room import get_room_info_raw, get_room_timetable_raw, Room
from requests import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browsermobproxy import Server
import time
import requests
import json
import pymysql
from bs4 import BeautifulSoup
import lxml


def _explain_response(data: List, attrs: List, need_upper: bool = True, is_enrollment: bool = False) -> List[Dict]:
    values = []
    try:
        for item in data:
            value = {}
            for attr in attrs:
                if need_upper:
                    value[attr[:1].upper() + attr[1:]] = item[attr]
                else:
                    value[attr] = item[attr]
                if is_enrollment:
                    value['InstructorName'] = item['classTimetableInstrVOList'][0]['instructorName']

            position = item.get('position')
            if position is not None:
                if need_upper:
                    value['RoomName'] += ('-' + position)
                else:
                    value['roomName'] += ('-' + position)
            values.append(value)
    except:
        pass
    return values


def split_time(str: str):
    if str == '':
        return None
    str = str.strip().replace("，", ",")
    final_period = []
    periods = str.split(',')
    for period in periods:
        time = period.split('-')
        if len(time) == 1:
            final_period.append(int(time[0]))
        else:
            final_period.extend(list(range(int(time[0]), int(time[1]) + 1)))
    return final_period


class CQUGetter:
    def __init__(self, sid=None, use_selenium=False, debug=False):
        self.authorization = None
        self.session = None
        self.is_success = False
        self.sid = sid
        self.use_selenium = use_selenium
        self.lib_key = None
        if self.use_selenium:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_server = Service('/usr/bin/chromedriver')
            self.server = Server('./CQU321/browsermob-proxy-2.1.4/bin/browsermob-proxy')
            self.server.start()
            self.proxy = self.server.create_proxy()
            chrome_options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
            chrome_options.add_argument('--ignore-certificate-errors')

            if not debug:
                chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=chrome_options, service=chrome_server)  # , service=chrome_server

    def is_match(self, username, password):
        if self.use_selenium:
            self.driver.get(
                'http://authserver.cqu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.cqu.edu.cn%2Fauthserver%2Fauthentication%2Fcas')
            username_element = self.driver.find_element(By.ID, 'username')
            password_element = self.driver.find_element(By.ID, 'password')
            # submit_element = driver.find_element(By.CLASS_NAME, 'auth_login_btn primary full_width')
            username_element.send_keys(username)
            password_element.send_keys(password + Keys.ENTER)
            # TODO:验证码出现时获取并重试登陆
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'content-blcok')))
            except:
                self.is_success = False
                return False
            else:
                self.is_success = True
                return True
        else:
            try:
                self.session = Session()
                login(self.session, username, password)
                self.authorization = access_mycqu(self.session)['Authorization']
            except:
                self.is_success = False
                return False
            else:
                self.is_success = True
                return True

    def pg_is_match(self, username, password):
        self.session = Session()
        data = {'userId': username, 'password': password, 'userType': 'student'}
        login_page = self.session.post(url='http://mis.cqu.edu.cn/mis/login.jsp', data=data)
        soup = BeautifulSoup(login_page.content, 'lxml')
        meta = soup.find('meta')['content']
        url = re.search(r'url=.*$', meta).group()
        if url[4:] == 'student.jsp':
            self.is_success = True
            return True
        else:
            self.is_success = False
            return False

    def get_score(self, connection, cursor, OpenId, need_all=False):
        if not self.is_success:
            return
        score_log = {}
        temp = {}
        if self.use_selenium:
            # TODO:将selenium成绩查询功能进行完全迁移
            try:
                self.driver.get('https://my.cqu.edu.cn/sam')
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'stu-sam-view-content')))
                token = self.driver.execute_script('return localStorage.getItem("cqu_edu_ACCESS_TOKEN");')
                assess_token = "Bearer " + token[1:-1]
            except:
                return
            else:
                headers = {
                    'Referer': 'https://my.cqu.edu.cn/sam/home',
                    'User-Agent': 'User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
                    'Authorization': assess_token
                }
                res = requests.get('http://my.cqu.edu.cn/api/sam/score/student/score', headers=headers)
                data = json.loads(res.content)['data']
        else:
            data = get_score_raw(self.session, False)

        for term, courses in data.items():
            temp[term] = _explain_response(courses['stuScoreHomePgVoS'], ['courseName', 'courseCode', 'courseCredit',
                                                                          'effectiveScoreShow', 'instructorName',
                                                                          'studyNature',
                                                                          'courseNature', 'id'])
            score_log[term] = [course for course in temp[term] if course['Id'] is not None]
            if not need_all:
                break
        for term, course in temp.items():
            for attrs in course:
                try:
                    if attrs['Id'] is None:
                        continue
                    if attrs['CourseCredit'] is None:
                        attrs['CourseCredit'] = -1
                    sql = "call insertScore(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (
                        OpenId, attrs['CourseName'], attrs['CourseCode'], float(attrs['CourseCredit']),
                        attrs['EffectiveScoreShow'], attrs['InstructorName'], attrs['StudyNature'],
                        attrs['CourseNature'], term))
                except:
                    with open('./insert_error.json', 'a') as f:
                        attrs['OpenId'] = OpenId
                        error_json = json.dumps(attrs)
                        f.write(error_json)
                    connection.rollback()
                else:
                    connection.commit()
        return score_log

    def pg_get_score(self):
        if not self.is_success:
            return
        score_page = self.session.get('http://mis.cqu.edu.cn/mis/student/plan/view.jsp')

        soup = BeautifulSoup(score_page.content, 'lxml')
        tables = soup.find_all('table')
        scores = tables[2].find_all('tr')
        del scores[0]
        score_log = []
        for score in scores:
            score_info = score.find_all('td')
            temp_list = []
            for info in score_info:
                info = info.text.strip()
                info = info.replace('\n', '')
                temp_list.append(info)
            if temp_list[7] == '':
                continue
            temp = {
                'Cid': temp_list[1],
                'Cname': temp_list[2],
                'Credit': temp_list[3],
                'Term': temp_list[5],
                'Year': temp_list[6],
                'Score': temp_list[7],
            }
            score_log.append(temp)
        return score_log

    def get_exam(self):
        if not self.is_success:
            return
        if self.use_selenium:
            self.proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
            try:
                self.driver.get('https://my.cqu.edu.cn/exam/home')
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'stu-exam-modal')))
            except:
                return
            else:
                result = self.proxy.har
                for entry in result['log']['entries']:
                    _url = entry['request']['url']
                    if "/api/exam/examTask/get-student-exam-list-outside" in _url:
                        _response = entry['response']
                        _content = _response['content']
                        _result = json.loads(_content['text'])
                        data = _result['data']['content']
                        exams = _explain_response(data,
                                                  ['roomName', 'startTime', 'endTime', 'courseName', 'courseCode',
                                                   'examDate', 'seatNum'])
                        self.proxy.close()
                        self.server.stop()
                        self.driver.quit()
                        return exams
        else:
            exam_raw = get_exam_raw(self.sid)['data']['content']
            exams = _explain_response(exam_raw,
                                      ['roomName', 'startTime', 'endTime', 'courseName', 'courseCode', 'examDate',
                                       'seatNum'])
            return exams

    def get_courses(self):
        if not self.is_success:
            return
        if self.use_selenium:
            self.proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
            try:
                self.driver.get('https://my.cqu.edu.cn/tt/AllCourseSchedule')
                list_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//*[@id="app"]/div/section/section/section/main/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div'))
                )
                ActionChains(driver=self.driver).click(list_element).perform()

                ActionChains(driver=self.driver).move_by_offset(0, 240).perform()
                ActionChains(driver=self.driver).click().perform()
                input_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//*[@id="app"]/div/section/section/section/main/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div')))
                ActionChains(driver=self.driver).click(input_element).perform()
                ActionChains(driver=self.driver).send_keys(self.sid).perform()
                # TODO: 将手动延时修改为自动延时
                ActionChains(driver=self.driver).move_by_offset(0, 80).perform()
                time.sleep(2)
                ActionChains(driver=self.driver).click().perform()
            except:
                return
            else:
                result = self.proxy.har
                for entry in result['log']['entries']:
                    _url = entry['request']['url']
                    if "/api/timetable/class/timetable/student/table-detail" in _url:
                        _response = entry['response']
                        _content = _response['content']
                        _result = json.loads(_content['text'])
                        data = _result['classTimetableVOList']
                        courses = _explain_response(data, ['weekDayFormat', 'courseName', 'courseCode', 'classNbr',
                                                           'roomName', 'instructorName', 'teachingWeekFormat',
                                                           'periodFormat', 'credit'])
                        self.proxy.close()
                        self.server.stop()
                        self.driver.quit()
                        return courses
        else:
            course_raw = get_course_raw(self.session, self.sid)
            courses = _explain_response(course_raw, ['weekDayFormat', 'courseName', 'courseCode', 'classNbr',
                                                     'roomName', 'instructorName', 'teachingWeekFormat',
                                                     'periodFormat', 'credit'])
            return courses

    def get_enrollment(self):
        if self.is_success:
            if self.use_selenium:
                # TODO:完善用selenium获取信息的部分
                return None
            else:
                try:
                    res = self.session.get(f'https://my.cqu.edu.cn/api/enrollment/timetable/student/{self.sid}')
                    data = json.loads(res.content)['data']
                    courses = _explain_response(data, ['weekDayFormat', 'courseName', 'courseCode', 'classNbr',
                                                       'roomName', 'teachingWeekFormat',
                                                       'periodFormat'], is_enrollment=True)
                except:
                    courses = None
                return courses

    def get_fees(self, isHuXi, room):
        if self.is_success:
            if self.use_selenium:
                # TODO:完善对应selenium的部分
                return None
            else:
                try:
                    access_card(self.session)
                    fees = get_fees_raw(self.session, isHuXi, room)['map']['data']
                    if isHuXi:
                        fees_info = {'Amount': fees['amount'], 'Eamount': fees['eamount'], 'Wamount': fees['wamount']}
                    else:
                        fees_info = {'Amount': fees['cashBalance'], 'Subsidies': fees['subsidiesBalance']}
                except:
                    fees_info = None
                return fees_info

    def get_gpa_ranking(self):
        if self.is_success:
            if self.use_selenium:
                return None
            else:
                try:
                    gpa_ranking = get_gpa_ranking_raw(self.session)
                except:
                    gpa_ranking = None

            return gpa_ranking

    def get_card(self):
        if self.is_success:
            if self.use_selenium:
                return None
            else:
                return_value = {}
                bills = []
                try:
                    access_card(self.session)
                    card_raw = get_card_raw(self.session)
                    amount = float(card_raw['acctAmt'] / 100)
                    account = card_raw['acctNo']
                    return_value['Amount'] = amount
                    bill_raw = get_bill_raw(self.session, account, 30)
                    for bill in bill_raw:
                        temp_bill = {'Money': float(bill['tranAmt'] / 100), 'Location': bill['mchAcctName'],
                                     'Time': bill['tranDt'], 'Type': bill['tranName']}
                        bills.append(temp_bill)
                    return_value['Bills'] = bills
                except:
                    return_value = None

                return return_value

    def get_person_info(self):
        if self.is_success:
            if self.use_selenium:
                return None
            else:
                url = "https://my.cqu.edu.cn/authserver/simple-user"
                res = self.session.get(url)
                data = json.loads(res.content)
                return_value = {
                    'Sid': data['code'],
                    'Name': data['name']
                }

                return return_value

    def get_borrow_list(self, is_curr):
        if self.is_success:
            if self.use_selenium:
                return None
            else:
                if self.lib_key is None:
                    self.lib_key = access_library(self.session)
                book_list = get_curr_books_raw(self.session, self.lib_key) \
                    if is_curr else get_history_books_raw(self.session, self.lib_key)
                temp = []
                for book in book_list:
                    book_info = {
                        'Id': book['bookId'],
                        'Title': book['title'],
                        'CallNo': book['callNo'],
                        'BorrowTime': book['borrowTime'],
                        'ShouldReturnTime': book.get('shouldReturnTime'),
                        'ReturnTime': book.get('returnTime'),
                        'LibraryName': book['libraryName'],
                        'RenewFlag': book['renewflag'],
                        'RenewCount': book['renewCount'],
                        'IsReturn': bool(book['cq']),
                    }
                    temp.append(book_info)

                return temp

    def renew_book(self, book_id):
        if self.lib_key is None:
            self.lib_key = access_library(self.session)

        info = BookInfo.renew_book(self.session, self.lib_key, book_id)
        statue = info['status']
        info = info['result']
        if statue == 500:
            return False, info
        elif statue == 200:
            return True, info

    def get_room(self, classroom):
        if self.is_success:
            if self.use_selenium:
                return None
            else:
                return_value = {'max_week': 0}
                teaching_list = []
                try:
                    room_info = get_room_info_raw(self.session, classroom)[0]
                    room_timetable = get_room_timetable_raw(self.session, classroom)['classTimetableVOList']
                except Exception as e:
                    return None
                for time_list in room_timetable:
                    # 将字符串以数组的形式导出
                    week_period = split_time(time_list['teachingWeekFormat'])
                    if week_period is None:
                        continue
                    if max(week_period) > return_value['max_week']:
                        return_value['max_week'] = max(week_period)
                    # all_week_period = list(set(all_week_period+week_period))
                    course_period = split_time(time_list['periodFormat'])
                    if course_period is None:
                        continue
                    weekday_list = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7}
                    time_list['weekDayFormat'] = weekday_list[time_list['weekDayFormat']]
                    teaching_schedule = {'id': time_list['courseName'], 'weeks': week_period,
                                         'week_day': time_list['weekDayFormat'], 'course_period': course_period}
                    teaching_list.append(teaching_schedule)
                return_value['room_name'] = classroom
                return_value['room_campus'] = room_info['campusName']
                return_value['room_building'] = room_info['buildingName']
                return_value['teaching_list'] = teaching_list
                # return_value['room_timetable'] = room_info
                return return_value


if __name__ == '__main__':
    # 139.155.183.8
    # 127.0.0.1
    connection = pymysql.connect(
        host='139.155.183.8',
        port=3306,
        user='CQU_321',
        password='CQUz5321',
        database='cqu_321'
    )
    cursor = connection.cursor()
    getter = CQUGetter(sid='20204051', use_selenium=False, debug=False)
    # getter.PG_is_match(username='202102131116t', password='19990422')

    if getter.is_match('07102028', 'Zhud125311'):
        print(getter.get_room('B二1715'))
    else:
        print('error')
