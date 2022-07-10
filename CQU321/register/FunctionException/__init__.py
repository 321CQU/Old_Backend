from .student_exception import *
from .homepage_exception import *
from .library_exception import *
from .announcement_exception import *
from .user_exception import *
from .cos_exception import *
from .forum_exception import *
from .school_info_exception import *

exception_list = {
    'get_course_process': GET_COURSE_EXCEPTION,
    'get_enrollment_process': GET_ENROLLMENT_EXCEPTION,
    'get_gpa_ranking_process': GET_GPA_RANKING_EXCEPTION,
    'get_score_process': GET_SCORE_EXCEPTION,

    'homepage_process': HOMEPAGE_EXCEPTION,

    'search_book_process': SEARCH_BOOK_EXCEPTION,
    'get_book_pos_process': GET_BOOK_POS_EXCEPTION,

    'get_group_info_process': GET_GROUP_INFO_EXCEPTION,
    'get_announcement_list_process': GET_ANNOUNCEMENT_LIST_EXCEPTION,
    'get_announcement_detail_process': GET_ANNOUNCEMENT_DETAIL_EXCEPTION,
    'subscribe_group_process': SUBSCRIBE_GROUP_EXCEPTION,
    'subscribe_list_process': SUBSCRIBE_LIST_EXCEPTION,

    'binding_auth_process': BINDING_AUTH_EXCEPTION,

    'get_cos_credential_process': GET_COS_CREDENTIAL_EXCEPTION,

    'send_post_process': SEND_POST_EXCEPTION,
    'update_post_process': UPDATE_POST_EXCEPTION,
    'get_post_list_process': GET_POST_LIST_EXCEPTION,
    'get_post_detail_process': GET_POST_DETAIL_EXCEPTION,
    'send_reply_process': SEND_REPLY_EXCEPTION,
    'get_reply_process': GET_REPLY_EXCEPTION,
    'delete_reply_process': DELETE_REPLY_EXCEPTION,

    'get_fees_process': GET_FEES_EXCEPTION,
}
