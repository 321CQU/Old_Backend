from .excepiton_info import *

__all__ = (
    'POST_JSON_ANALYSES_EXCEPTION', 'GET_COURSE_EXCEPTION', 'GET_ENROLLMENT_EXCEPTION', 'GET_GPA_RANKING_EXCEPTION',
    'GET_SCORE_EXCEPTION'
)

POST_JSON_ANALYSES_EXCEPTION = dict([
    invalid_key_exception_info, unsupport_version_exception_info, incorrect_params_exception_info
])

GET_COURSE_EXCEPTION = POST_JSON_ANALYSES_EXCEPTION.copy()
GET_COURSE_EXCEPTION.update(dict([
    info_is_null_exception_info, incorrect_login_credentials_exception_info
]))

GET_ENROLLMENT_EXCEPTION = GET_COURSE_EXCEPTION

GET_GPA_RANKING_EXCEPTION = POST_JSON_ANALYSES_EXCEPTION.copy()
GET_GPA_RANKING_EXCEPTION.update(dict([
    incorrect_login_credentials_exception_info, cqu_website_error_exception_info
]))

GET_SCORE_EXCEPTION = GET_COURSE_EXCEPTION.copy()
GET_SCORE_EXCEPTION.update(dict([
    openid_access_error_exception_info,
]))
