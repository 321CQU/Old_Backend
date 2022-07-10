import json
import requests

data = {'Key': 'CQUz5321',
        'Sid': '20204051'}
mail_data = {'Key': 'CQUz5321',
             'Sid': '20204051',
             'Mail': '2961163526@qq.com',
             'Fid': '51,52,53,64,65,67,68,69,70,71'}
user_data = {'Key': 'CQUz5321',
             'Sid': '20204051',
             'UserName': 'Zhulegend',
             'UserImg': 'https://thirdwx.qlogo.cn/mmopen/vi_32/JM94ehUicQMdmXo7QYHFicRpoXu8foQXmkKtRaFQGjnSLevZmib1RQzjF8Dbf3Jw1WOCrzlwibGVia5Bicqs6PYlG5iaA/132'}
send_feedback_data = {'Key': 'CQUz5321',
                      'Sid': '20204051',
                      'Content': '框架切换测试'}
get_feedback_data = {'Key': 'CQUz5321',
                     # 'Limit': '2,1'
                     }
login_data = {
    'Key': 'CQUz5321',
    'Sid': '20204051',
    'UserName': '07102028',
    'Password': 'Zhud125311',
    'Code': 'test',
    'NeedAll': False,
    'Debug': True,
    'IsHuXi': False,
    'Room': 'B6S106',
}

subscribe_data = {
    'Key': 'CQUz5321',
    'OpenId': 'test',
    'Sid': '20204051',
    'UserName': '07102028',
    'Password': 'Zhud125311'
}

test_data = {
    'Key': 'CQUz5321',
    'Data': {
        'Score': 80,
        'Name': '测试科目'
    }
}

send_comment_data = {
    'Key': 'CQUz5321',
    'FBid': '15',
    'Sid': '20204051',
    'Content': 'test comment'
}

get_comment_data = {
    'Key': 'CQUz5321',
    'FBid': 352
}

pg_data = {
    'Key': 'CQUz5321',
    'UserName': '202102131116t',
    'Password': '19990422'
}

get_course_list_data = {
    'Key': 'CQUz5321',
    'CourseName': '马克思'
}

get_course_detail_data = {
    'Key': 'CQUz5321',
    'Cid': 'CHEM20033'
}

send_post_data = {
    'Key': 'CQUz5321',
    'Title': 'title test',
    'Content': 'content test',
    'Type': 'normal',
    'Author': '20204051'
}

update_post_data = {
    'Key': 'CQUz5321',
    'Title': 'title test',
    'Content': 'content test',
    'IsDelete': True,
    'Pid': 9,
    'Sid': '20201682',
}

get_post_list_data = {
    'Key': 'CQUz5321',
    'Type': 'all',
}

get_post_detail_data = {
    'Key': 'CQUz5321',
    'Pid': 527,
}

get_fees_data = {
    'Key': 'CQUz5321',
    'UserName': '07102028',
    'Password': 'Zhud125311',
    'IsHuXi': True,
    'Room': 'b5321',
}

pull_custom_event_data = {
    'Key': 'CQUz5321',
    'Code': 'oUkKe5OPOlDjKVdnFRx5Gbl3SKsY'
}

push_custom_event_data = {
    'Key': 'CQUz5321',
    'Code': 'test',
    'Events': [
        {
            'CEcode': 'test1',
            'CEname': 'test1',
            'PeriodFormat': 'test1',
            'TeachingWeekFormat': 'test1',
            'WeekdayFormat': 'test1',
            'Content': 'test1',
        },
        {
            'CEcode': 'test2',
            'CEname': 'test2',
            'PeriodFormat': 'test2',
            'TeachingWeekFormat': 'test2',
            'WeekdayFormat': 'test2',
            'Content': 'test2',
        },
    ]
}

send_reply_data = {
    'Key': 'CQUz5321',
    'Content': "test",
    'Pid': 9,
    'Author': '20204051'
}

get_reply_data = {
    'Key': 'CQUz5321',
    'Pid': 9
}

delete_reply_data = {
    'Key': 'CQUz5321',
    'Rid': 1,
    'Sid': '20204051'
}

library_data = {
    'Key': 'CQUz5321',
    'UserName': '07102028',
    'Password': 'Zhud125311',
    'IsCurr': False,
    'BookId': '31506059064786'
}

get_vacant_room_data = {
    'Key': 'CQUz5321',
    'Sid': '20204051',
    'UserName': '07102028',
    'Password': 'Zhud125311',
    'AppointWeek': '1-4',
    'AppointWeekday': 5,
    'AppointBuilding': 'A区2教',
    'AppointCourse': '1-2',

}
update_user_info_data = {
    'Key': 'CQUz5321',
    'Code': 'test',
    'Sid': '20204051',
    'Auth': '07102028',
    'Password': 'Z',
    'Email': 'test',
    'Dormitory': 'test_d'
}

homepage_data = {
    'Key': 'CQUz5321',
    'Version': '2.0',
    'Params': {}
}

# 'http://127.0.0.1:8000/321CQU/'
online_url = 'http://www.zhulegend.com/321CQU'
local_url = 'http://127.0.0.1:8000/321CQU'

stuVal_url = '/student/StuVal'
total_duration_url = '/student/total_duration'
all_activity_url = '/student/all_activity'

send_volunteer_pdfs_url = '/mail/send_volunteer_pdfs'

set_user_info_url = '/user/set_info'
advertise_url = '/user/advertise/look'
get_advertise_times_url = '/user/advertise/times'
login_url = '/user/login'
update_user_info_url = '/user/update_user_info'
select_user_info_url = '/user/select_user_info'
delete_user_info_url = '/user/delete_user_info'

send_feedback_url = '/feedback/send'
get_feedback_url = '/feedback/get'
send_comment_url = '/feedback/send_comment'
get_comment_url = '/feedback/get_comment'

get_score_url = '/student/get_score'
get_exam_url = '/student/get_exam'
get_course_url = '/student/get_course'
get_enrollment_url = '/student/get_enrollment'
get_gpa_rankin_url = '/student/get_gpa_ranking'

mess_val_url = '/message'
subscribe_url = '/message/subscribe'

add_custom_event_url = '/course_table/add_custom_event'
update_custom_event_url = '/course_table/update_custom_event'
get_custom_event_url = '/course_table/get_custom_event'
pull_custom_event_url = '/course_table/pull_custom_event'
push_custom_event_url = '/course_table/push_custom_event'

about_me_url = '/about/about_us'
get_tutorials_url = '/about/get_tutorials'

test_data_url = '/test_data'

pg_is_match_url = '/pg_student/is_match'
pg_get_score_url = '/pg_student/get_score'

get_course_list_url = '/school_info/get_course_list'
get_course_detail_url = '/school_info/get_course_detail'
get_fees_info_url = '/school_info/get_fees'
get_curr_term_url = '/school_info/get_curr_term'
get_next_term_url = '/school_info/get_next_term'
get_card_url = '/school_info/get_card'
get_vacant_room_url = '/school_info/get_vacant_room'
get_vacant_room_url_old_campus = '/school_info/get_vacant_room_old_campus'

send_post_url = '/forum/send_post'
update_post_url = '/forum/update_post'
get_post_list_url = '/forum/get_post_list'
get_post_detail_url = '/forum/get_post_detail'
send_reply_url = '/forum/send_reply'
get_reply_url = '/forum/get_reply'
delete_reply_url = '/forum/delete_reply'

homepage_url = '/homepage'

get_borrow_list_url = '/library/get_borrow_list'
renew_book_url = '/library/renew_book'
search_book_url = '/library/search_book'
get_book_pos_url = '/library/get_book_pos'

api_url = '/api'

api_data = {
    'Key': 'CQUz5321',
    'Version': '2.4.0',
}

if __name__ == '__main__':
    post_json = json.dumps(login_data)
    res_json = requests.post(local_url + get_exam_url, post_json)
    if res_json.status_code == 200:
        res = json.loads(res_json.content)
        print(res)
    elif res_json.status_code == 404:
        print('Connect error')
    else:
        print(res_json.status_code)

# post_json = json.dumps(get_vacant_room_data)
# res_json = requests.post(local_url + get_vacant_room_url, post_json)
# if res_json.status_code == 200:
#     res = json.loads(res_json.content)
#     print(res)
# elif res_json.status_code == 404:
#     print('Connect error')
# else:
#     print(res_json.status_code)
# res = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential',
#                    params={'appid': 'wx35453b42735393ed', 'secret': '7169cbd76cd6eeaaff0ab5fdbcaac613'})
# print(json.loads(res.content))

