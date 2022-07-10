from .student_returns import *
from .homepage_returns import *
from .library_returns import *
from .announcement_returns import *
from .user_returns import *
from .cos_returns import *
from .forum_returns import *
from .school_info_returns import *

return_list = {
    'get_course_process': GET_COURSE_RETURN,
    'get_enrollment_process': GET_ENROLLMENT_RETURN,
    'get_gpa_ranking_process': GET_GPA_RANKING_RETURN,
    'get_score_process': GET_SCORE_RETURN,

    'homepage_process': HOMEPAGE_RETURN,

    'search_book_process': SEARCH_BOOK_RETURNS,
    'get_book_pos_process': GET_BOOK_POS_RETURNS,

    'get_group_info_process': GET_GROUP_INFO_RETURNS,
    'get_announcement_list_process': GET_ANNOUNCEMENT_LIST_RETURNS,
    'get_announcement_detail_process': GET_ANNOUNCEMENT_DETAIL_RETURNS,
    'subscribe_group_process': SUBSCRIBE_GROUP_RETURNS,
    'subscribe_list_process': SUBSCRIBE_LIST_RETURNS,

    'binding_auth_process': BINDING_AUTH_RETURNS,

    'get_cos_credential_process': GET_COS_CREDENTIAL_RETURNS,

    'send_post_process': SEND_POST_RETURNS,
    'update_post_process': UPDATE_POST_RETURNS,
    'get_post_list_process': GET_POST_LIST_RETURNS,
    'get_post_detail_process': GET_POST_DETAIL_RETURNS,
    'send_reply_process': SEND_REPLY_RETURNS,
    'get_reply_process': GET_REPLY_RETURNS,
    'delete_reply_process': DELETE_REPLY_RETURNS,

    'get_fees_process': GET_FEES_RETURNS,
}
