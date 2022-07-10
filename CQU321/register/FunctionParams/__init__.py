from .. import ParamsInfo
from .student_params import *
from .homepage_params import *
from .library_params import *
from .announcement_params import *
from .user_params import *
from .cos_params import *
from .forum_params import *
from .school_info_params import *

params_list = {
    'get_course_process': GET_COURSE_PARAMS,
    'get_enrollment_process': GET_ENROLLMENT_PARAMS,
    'get_gpa_ranking_process': GET_GPA_RANKING_PARAMS,
    'get_score_process': GET_SCORE_PARAMS,

    'homepage_process': HOMEPAGE_PARAMS,

    'search_book_process': SEARCH_BOOK_PARAMS,
    'get_book_pos_process': GET_BOOK_POS_PARAMS,

    'get_group_info_process': GET_GROUP_INFO_PARAMS,
    'get_announcement_list_process': GET_ANNOUNCEMENT_LIST_PARAMS,
    'get_announcement_detail_process': GET_ANNOUNCEMENT_DETAIL_PARAMS,
    'subscribe_group_process': SUBSCRIBE_GROUP_PARAMS,
    'subscribe_list_process': SUBSCRIBE_LIST_PARAMS,

    'binding_auth_process': BINDING_AUTH_PARAMS,

    'get_cos_credential_process': GET_COS_CREDENTIAL_PARAMS,

    'send_post_process': SEND_POST_PARAMS,
    'update_post_process': UPDATE_POST_PARAMS,
    'get_post_list_process': GET_POST_LIST_PARAMS,
    'get_post_detail_process': GET_POST_DETAIL_PARAMS,
    'send_reply_process': SEND_REPLY_PARAMS,
    'get_reply_process': GET_REPLY_PARAMS,
    'delete_reply_process': DELETE_REPLY_PARAMS,

    'get_fees_process': GET_FEES_PARAMS,
}
