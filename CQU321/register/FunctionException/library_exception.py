from .excepiton_info import *

SEARCH_BOOK_EXCEPTION = dict([
    invalid_key_exception_info, unsupport_version_exception_info, incorrect_params_exception_info,
    incorrect_login_credentials_exception_info,
])

GET_BOOK_POS_EXCEPTION = SEARCH_BOOK_EXCEPTION.copy()
