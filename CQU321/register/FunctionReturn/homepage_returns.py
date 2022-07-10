from typing import List, Dict

from .. import ParamsInfo

HOMEPAGE_RETURN = {
    '1.0': [
        ParamsInfo(
            'PictureUrls', List, '首页图片链接地址列表',
            [ParamsInfo('Urls', str, '图片链接地址', name_is_key=False)]
        ),
        ParamsInfo(
            'LastUpdate', str, '最后更新时间'
        ),
    ],
    '2.0': [
        ParamsInfo(
            'Pictures', List, '首页图片相关信息', [
                ParamsInfo('Url', str, '图片获取路径'),
                ParamsInfo('ContentUrl', str, '跳转路径（当无对应内容时为None）', can_be_none=True),
                ParamsInfo('JumpType', str, '跳转类型（markdown为"md"，模块为"mk"）', can_be_none=True)
            ]
        ),
        ParamsInfo(
            'LastUpdate', str, '最后更新时间'
        ),
    ],
    '2.1': [
        ParamsInfo(
            'Pictures', List, '首页图片相关信息', [
                ParamsInfo('Url', str, '图片获取路径'),
                ParamsInfo('ContentUrl', str, '跳转路径（当无对应内容时为None）', can_be_none=True),
                ParamsInfo('JumpType', str, '跳转类型（markdown为"md"，模块为"mk"）', can_be_none=True)
            ]
        ),
        ParamsInfo(
            'LastUpdate', str, '最后更新时间'
        ),
    ]
}
