from .excepiton_info import *

GET_ANNOUNCEMENT_LIST_EXCEPTION = dict([
    invalid_key_exception_info, unsupport_version_exception_info, incorrect_params_exception_info,
])

GET_ANNOUNCEMENT_DETAIL_EXCEPTION = GET_ANNOUNCEMENT_LIST_EXCEPTION.copy()

GET_GROUP_INFO_EXCEPTION = GET_ANNOUNCEMENT_LIST_EXCEPTION.copy()
GET_GROUP_INFO_EXCEPTION.update(dict([user_not_found]))

SUBSCRIBE_GROUP_EXCEPTION = GET_GROUP_INFO_EXCEPTION.copy()

SUBSCRIBE_LIST_EXCEPTION = GET_GROUP_INFO_EXCEPTION.copy()
