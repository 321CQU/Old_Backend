from django.urls import path
from .views import api_views, about_views, message_views, student_views, mail_views, user_views, feedback_views, \
    test_view, pg_student_views, school_info_views, data_follow_view, forum_views, course_table_view, homepage_view, \
    library_views, announcement_views, cos_views

urlpatterns = [
    # 321CQU api接口界面
    path('api', api_views.api_page, name='api_page'),
    path('test_data', test_view.test_data, name='test_data'),

    # 学校相关信息查询
    path('school_info/get_curr_term', school_info_views.get_curr_term, name='get_curr_term'),
    path('school_info/get_next_term', school_info_views.get_next_term, name='get_next_term'),
    path('school_info/get_course_list', school_info_views.get_course_list, name='get_course_list'),
    path('school_info/get_course_detail', school_info_views.get_course_detail, name='get_course_detail'),
    path('school_info/get_fees', school_info_views.get_fees, name='get_fees'),
    path('school_info/get_card', school_info_views.get_card, name='get_card'),
    path('school_info/get_vacant_room', school_info_views.get_vacant_room, name='get_vacant_room'),
    path('school_info/get_vacant_room_old_campus', school_info_views.get_vacant_room_old_campus, name='get_vacant_room_old_campus'),


    # 321CQU about界面（未来可能用于各种协议的更新等）
    path('about/about_us', about_views.about_us, name='about_us'),
    path('about/get_tutorials', about_views.get_tutorials, name='get_tutorials'),

    # 首页广告图片信息
    path('homepage', homepage_view.homepage, name='homepage'),

    # 321CQU 小程序消息推送
    path('message', message_views.message_validation, name='mess_val'),
    path('message/subscribe', message_views.subscribe_message, name='subscribe'),

    # 课表相关功能
    path('course_table/pull_custom_event', course_table_view.pull_custom_event, name='pull_custom_event'),
    path('course_table/push_custom_event', course_table_view.push_custom_event, name='push_custom_event'),

    # 学生相关信息查询
    path('student/StuVal', student_views.student_validation, name='stuVal'),
    path('student/total_duration', student_views.total_duration, name='total_duration'),
    path('student/all_activity', student_views.all_activity, name='all_activity'),
    path('student/get_score', student_views.get_score, name='get_score'),
    path('student/get_exam', student_views.get_exam, name='get_exam'),
    path('student/get_course', student_views.get_course, name='get_course'),
    path('student/get_enrollment', student_views.get_enrollment, name='get_enrollment'),
    path('student/get_gpa_ranking', student_views.get_gpa_ranking, name='get_gpa_ranking'),

    # 图书馆相关
    path('library/get_borrow_list', library_views.get_borrow_list, name='get_borrow_list'),
    path('library/renew_book', library_views.renew_book, name='renew_book'),
    path('library/search_book', library_views.search_book, name='search_book'),
    path('library/get_book_pos', library_views.get_book_pos, name='get_book_pos'),

    # 研究生相关信息查询
    path('pg_student/is_match', pg_student_views.pg_is_match, name='pg_is_match'),
    path('pg_student/get_score', pg_student_views.pg_get_score, name='pg_get_score'),

    # 服务器收发邮件
    path('mail/send_volunteer_pdfs', mail_views.send_volunteer_pdfs, name='send_volunteer_pdfs'),

    # 小程序用户管理
    path('user/set_info', user_views.set_info, name='set_user_info'),
    path('user/login', user_views.is_match, name='is_match'),
    path('user/bind', user_views.binding_auth, name='bind_auth'),
    path('user/advertise/look', user_views.after_advertise, name='after_advertise'),
    path('user/advertise/times', user_views.get_advertise_times, name='get_advertise_times'),
    path('user/update_user_info', user_views.update_user_info, name='update_user_info'),
    path('user/select_user_info', user_views.select_user_info, name='select_user_info'),
    path('user/delete_user_info', user_views.delete_user_info, name='delete_user_info'),

    # 小程序反馈相关
    path('feedback/send', feedback_views.send_feedback, name='send_feedback'),
    path('feedback/get', feedback_views.get_feedback, name='get_feedback'),
    path('feedback/send_comment', feedback_views.send_comment, name='send_comment'),
    path('feedback/get_comment', feedback_views.get_comment, name='get_comment'),

    # 论坛相关功能
    path('forum/send_post', forum_views.send_post, name='send_post'),
    path('forum/update_post', forum_views.update_post, name='update_post'),
    path('forum/get_post_list', forum_views.get_post_list, name='get_post_list'),
    path('forum/get_post_detail', forum_views.get_post_detail, name='get_post_detail'),
    path('forum/get_reply', forum_views.get_reply, name='get_reply'),
    path('forum/send_reply', forum_views.send_reply, name='send_reply'),
    path('forum/delete_reply', forum_views.delete_reply, name='delete_reply'),

    # 活动公告相关
    path('announcement/get_list', announcement_views.get_announcement_list, name='get_announcement_list'),
    path('announcement/get_detail', announcement_views.get_announcement_detail, name='get_announcement_detail'),
    path('announcement/group/get_info', announcement_views.get_group_info, name='get_group_info'),
    path('announcement/group/subscribe', announcement_views.subscribe_group, name='subscribe_group'),
    path('announcement/group/subscribe/list', announcement_views.subscribe_list, name='subscribe_list'),

    # 对象存储相关
    path('cos/get_credential', cos_views.get_cos_credential, name='get_cos_credential'),

    # 相关数据跟踪:
    path('data', data_follow_view.data_follow, name='data_follow'),
]
