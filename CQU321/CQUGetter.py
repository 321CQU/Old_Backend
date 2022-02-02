# 这一部分为网站正在使用的CQUGetter，我另一个项目发布的CQUGetter相较于这里使用的更加规范且具有通用性

import re
from typing import List, Dict, Any, Union, Optional
from mycqu.auth import login
from mycqu.mycqu import access_mycqu
from mycqu.exam import get_exam_raw
from mycqu.course import get_course_raw
from mycqu.score import get_score_raw
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
            values.append(value)
    except:
        pass
    return values


class CQUGetter:
    def __init__(self, sid=None, use_selenium=False, debug=False):
        self.authorization = None
        self.session = None
        self.is_success = False
        self.sid = sid
        self.use_selenium = use_selenium
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
            data = get_score_raw(self.session)

        for term, courses in data.items():
            temp[term] = _explain_response(courses['stuScoreHomePgVoS'], ['courseName', 'courseCode', 'courseCredit',
                                                     'effectiveScoreShow', 'instructorName', 'studyNature',
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
