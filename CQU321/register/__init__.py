from __future__ import annotations

from typing import List, Dict

from CQU321.register.ParamsInfo import ParamsInfo, verify_params_info_list
from CQU321.register import FunctionException, FunctionParams, FunctionReturn
from CQU321.register.WebsiteExpection import UnregisteredException, UnSupportVersion, IncorrectParams

FUNC_EXCEPTION_LIST = {
    'post_json_analyses': FunctionException.POST_JSON_ANALYSES_EXCEPTION,
}
FUNC_EXCEPTION_LIST.update(FunctionException.exception_list)
FUNC_PARAMS_LIST = FunctionParams.params_list
FUNC_RETURN_LIST = FunctionReturn.return_list


def get_params_info_by_name(func_name: str, version: str, is_return_params: bool) -> List[ParamsInfo]:
    if is_return_params:
        data = FUNC_RETURN_LIST.get(func_name)
    else:
        data = FUNC_PARAMS_LIST.get(func_name)

    # 可能是不必要的错误处理
    if data is None:
        raise UnregisteredException

    result = data.get(version)

    if result is None:
        raise UnSupportVersion

    return result


def verify_data_same_as_registered(data: Dict, func_name: str, version: str, is_return_params: bool):
    register_params = get_params_info_by_name(func_name, version, is_return_params)
    # TODO: 有可选参数时进行参数数量校验
    # if len(register_params) != len(data):
    #     raise IncorrectParams(f"input or output func params length didn't match")
    verify_params_info_list(data, register_params)


