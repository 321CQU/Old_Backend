from .excepiton_info import *

SEND_POST_EXCEPTION = dict([
    invalid_key_exception_info, unsupport_version_exception_info, incorrect_params_exception_info,
    user_not_found, no_authority
])

UPDATE_POST_EXCEPTION = SEND_POST_EXCEPTION.copy()

GET_POST_LIST_EXCEPTION = SEND_POST_EXCEPTION.copy()

GET_POST_DETAIL_EXCEPTION = SEND_POST_EXCEPTION.copy()

SEND_REPLY_EXCEPTION = SEND_POST_EXCEPTION.copy()

GET_REPLY_EXCEPTION = SEND_POST_EXCEPTION.copy()

DELETE_REPLY_EXCEPTION = SEND_POST_EXCEPTION.copy()
