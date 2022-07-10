from typing import List

from .. import ParamsInfo

GET_ANNOUNCEMENT_LIST_RETURNS = {
    '2.0': [
        ParamsInfo('Announcements', List, '公告列表', [
            ParamsInfo('Aid', int, '公告ID'),
            ParamsInfo('Title', str, '公告标题'),
            ParamsInfo('Name', str, '公告发布组织名称'),
            ParamsInfo('CoverUrl', str, '活动封面地址', can_be_none=True),
            ParamsInfo('StartDate', str, '活动开始日期（0000-00-00表示无开始日期）'),
            ParamsInfo('EndDate', str, '活动结束日期（0000-00-00表示无开始日期）'),
            ParamsInfo('UpdateDate', str, '公告发布日期'),
        ]),
    ],
    '2.1': [
        ParamsInfo('Announcements', List, '公告列表', [
            ParamsInfo('Aid', int, '公告ID'),
            ParamsInfo('Title', str, '公告标题'),
            ParamsInfo('Name', str, '公告发布组织名称'),
            ParamsInfo('CoverUrl', str, '活动封面地址', can_be_none=True),
            ParamsInfo('StartDate', str, '活动开始日期（0000-00-00表示无开始日期）'),
            ParamsInfo('EndDate', str, '活动结束日期（0000-00-00表示无开始日期）'),
            ParamsInfo('UpdateDate', str, '公告发布日期'),
        ]),
    ],
}

GET_ANNOUNCEMENT_DETAIL_RETURNS = {
    '2.0': [
        ParamsInfo('Markdown', str, '公告正文'),
    ],
}

GET_GROUP_INFO_RETURNS = {
    '2.0': [
        ParamsInfo('Avatar', str, '组织头像链接，当为None时表示无头像', can_be_none=True),
    ],
}

SUBSCRIBE_GROUP_RETURNS = {
    '2.0': [],
}

SUBSCRIBE_LIST_RETURNS = {
    '2.0': [
        ParamsInfo('Group', List, '订阅的组织', [
            ParamsInfo('GroupName', str, '组织名称')
        ])
    ],
}


