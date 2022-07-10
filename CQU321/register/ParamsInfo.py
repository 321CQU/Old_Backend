from __future__ import annotations
from functools import reduce

from typing import List, Dict

from CQU321.register.WebsiteExpection import IncorrectParams

__all__ = ['ParamsInfo', 'verify_params_info_list']


class ParamsInfo:
    """
    用于执行变量类型检查和自动格式化输出变量内容的类
    """
    def __init__(self, name: str, cls, introduction: str, sub_params: List[ParamsInfo] = None,
                 is_optional: bool = False, can_be_none: bool = False, name_is_key: bool = True):
        """
        :param name: 变量所在字典对应键的名称
        :param cls: 变量类型
        :param introduction: 变量介绍（用于格式化输出变量内容）
        :param sub_params: 变量所拥有的子变量（当变量为List或Dict时，可以填写该参数，对变量"内部参数"进行类型检查）
        :param is_optional: 变量是否可选（可选时，未发现该变量不会导致报错）
        :param can_be_none: 变量是否可以为None值
        :param name_is_key: 变量名是否作为字典键名（当变量类型为List时，其子变量不具有事实上当名称，此时应当设置子变量该参数为False）
        """
        self.name = name
        self.cls = cls
        self.introduction = introduction
        self.sub_params = sub_params
        self.is_optional = is_optional
        self.can_be_none = can_be_none
        self.name_is_key = name_is_key

    def __len__(self):
        result = 1
        if self.cls == List and self.sub_params is not None:
            for param in self.sub_params:
                result += len(param)
            result -= 1
        return result

    def check(self, data):
        """
        比较对应数据是否满足该ParamsInfo类的要求
        """
        if self.can_be_none:
            try:
                data[self.name]
            except:
                raise IncorrectParams(f"Except a params(name: {self.name}, cls: {self.cls}) "
                                      f"which can be None, but don't found")
            else:
                return

        if not self.name_is_key:
            if self.cls == Dict or self.cls == List:
                if self.sub_params is None:
                    raise IncorrectParams(f'Except {self.name} has sub_params but found None')
                for _, value in data.items():
                    if self.cls == List:
                        for sub_data in value:
                            verify_params_info_list(sub_data, self.sub_params)
                    elif self.cls == Dict:
                        verify_params_info_list(value, self.sub_params)
            else:
                if not isinstance(data, self.cls):
                    raise IncorrectParams(f"Except data is {self.cls} but don't match")

            return

        if isinstance(data.get(self.name), self.cls):
            if self.sub_params is not None and self.cls == List:
                for sub_data in data.get(self.name):
                    # if len(self) != len(sub_data):
                    #     raise IncorrectParams(f"Except params(name: {self.name}, cls: {self.cls}) "
                    #                           f"have {len(self)} params, but have {len(sub_data)}")
                    verify_params_info_list(sub_data, self.sub_params)

            if self.sub_params is not None and self.cls == Dict:
                verify_params_info_list(data.get(self.name), self.sub_params)

            return

        if self.is_optional and data.get(self.name) is None:
            return

        raise IncorrectParams(f"Param(name: {self.name}, cls: {self.cls}, "
                              f"is_optional: {self.is_optional}, can_be_None: {self.can_be_none}) don't found")

    def print(self, parent_info_names: List[str] = None) -> List[Dict]:
        """
        格式化输出ParamInfo对象到字典，用于接口页面生成
        """
        result = []
        if self.sub_params is not None and (self.cls == List or self.cls == Dict):
            for param in self.sub_params:
                if parent_info_names and parent_info_names[-1] != self.name:
                    parent_info_names.append(self.name)
                result.extend(param.print(parent_info_names if parent_info_names else [self.name]))
        else:
            temp = {
                'name': self.name + (('(' + reduce(lambda x, y: x + '-> ' + y, parent_info_names) + ')')
                                     if parent_info_names else '') + (' (Optional)' if self.is_optional else ''),
                'cls': self.cls.__name__,
                'info': self.introduction
            }
            result.append(temp)

        return result


def verify_params_info_list(data: Dict, param_infos: List[ParamsInfo]):
    for param_info in param_infos:
        param_info.check(data)
