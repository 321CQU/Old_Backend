from django.urls import path
from .views import api_views, about_views, message_views, student_views, mail_views, user_views, feedback_views, \
    test_view, pg_student_views, school_info_views

urlpatterns = [
    # 321CQU api接口界面
    path('api', api_views.api_page, name='api_page'),
    path('test_data', test_view.test_data, name='test_data'),

    # 学校相关信息查询
    path('school_info/get_curr_term', school_info_views.get_curr_term, name='get_curr_term'),
    path('school_info/get_next_term', school_info_views.get_next_term, name='get_next_term'),

    # 321CQU about界面（未来可能用于各种协议的更新等）
    path('about/about_us', about_views.about_us, name='about_us'),

    # 321CQU 小程序消息推送
    path('message', message_views.message_validation, name='mess_val'),
    path('message/subscribe', message_views.subscribe_message, name='subscribe'),

    # 学生相关信息查询
    path('student/StuVal', student_views.student_validation, name='stuVal'),
    path('student/total_duration', student_views.total_duration, name='total_duration'),
    path('student/all_activity', student_views.all_activity, name='all_activity'),
    path('student/get_score', student_views.get_score, name='get_score'),
    path('student/get_exam', student_views.get_exam, name='get_exam'),
    path('student/get_course', student_views.get_course, name='get_course'),
    path('student/get_enrollment', student_views.get_enrollment, name='get_enrollment'),

    # 研究生相关信息查询
    path('pg_student/is_match', pg_student_views.pg_is_match, name='pg_is_match'),
    path('pg_student/get_score', pg_student_views.pg_get_score, name='pg_get_score'),

    # 服务器收发邮件
    path('mail/send_volunteer_pdfs', mail_views.send_volunteer_pdfs, name='send_volunteer_pdfs'),

    # 小程序用户管理
    path('user/set_info', user_views.set_info, name='set_user_info'),
    path('user/login', user_views.is_match, name='is_match'),

    # 小程序反馈相关
    path('feedback/send', feedback_views.send_feedback, name='send_feedback'),
    path('feedback/get', feedback_views.get_feedback, name='get_feedback'),
    path('feedback/send_comment', feedback_views.send_comment, name='send_comment'),
    path('feedback/get_comment', feedback_views.get_comment, name='get_comment'),
]
