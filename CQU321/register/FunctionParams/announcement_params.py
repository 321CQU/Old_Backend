from .. import ParamsInfo

GET_ANNOUNCEMENT_LIST_PARAMS = {
    '2.0': [
        ParamsInfo('Page', int, '页数（20条公告为一页，从0开始）'),
    ],
    '2.1': [
        ParamsInfo('Page', int, '页数（20条公告为一页，从0开始）'),
        ParamsInfo('Type', str, 'normal--不进行筛选，subscribe--仅展示订阅的组织，group--展示所在组织的所有活动（包括未公开），'
                                '不为三者中的某一值时，报IncorrectParams错误'),
        ParamsInfo('Sid', str, '学号')
    ],
}

GET_ANNOUNCEMENT_DETAIL_PARAMS = {
    '2.0': [
        ParamsInfo('Id', int, '需要获取的公告详情的id'),
    ],
}

GET_GROUP_INFO_PARAMS = {
    '2.0': [
        ParamsInfo('Name', str, '需要获取信息的组织名')
    ]
}

SUBSCRIBE_GROUP_PARAMS = {
    '2.0': [
        ParamsInfo('Sid', str, '学号'),
        ParamsInfo('Type', int, '操作类型，为0表示取消订阅，为1表示订阅'),
        ParamsInfo('GroupName', str, '关注/取关组织名'),
    ]
}

SUBSCRIBE_LIST_PARAMS = {
    '2.0': [
        ParamsInfo('Sid', str, '学号'),
    ]
}
