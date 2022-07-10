from CQU321.register import ParamsInfo

SEND_POST_PARAMS = {
    '1.0': [
        ParamsInfo('Title', str, '标题'),
        ParamsInfo('Content', str, '内容（不超过1000个字符）'),
        ParamsInfo('Type', str, '分区'),
        ParamsInfo('Author', str, '发帖人学号')
    ],
    '2.0': [
        ParamsInfo('Title', str, '标题'),
        ParamsInfo('Content', str, '内容（不超过1000个字符）'),
        ParamsInfo('Type', str, '分区'),
        ParamsInfo('Author', str, '发帖人学号'),
        ParamsInfo('IsAnonymous', bool, '是否匿名，为1则匿名，为0则不匿名')
    ]
}

UPDATE_POST_PARAMS = {
    '1.0': [
        ParamsInfo('Title', str, '标题'),
        ParamsInfo('Content', str, '内容'),
        ParamsInfo('IsDelete', bool, '是否为删除帖子'),
        ParamsInfo('Pid', int, '帖子序号'),
        ParamsInfo('Sid', str, '操作者学号（仅有发帖人、分区管理员、超级管理员可以删帖）')
    ],
    '2.0': [
        ParamsInfo('Title', str, '标题'),
        ParamsInfo('Content', str, '内容'),
        ParamsInfo('IsDelete', bool, '是否为删除帖子'),
        ParamsInfo('Pid', int, '帖子序号'),
        ParamsInfo('Sid', str, '操作者学号（仅有发帖人、分区管理员、超级管理员可以删帖）'),
        ParamsInfo('IsAnonymous', bool, '是否匿名，为1则匿名，为0则不匿名'),
    ]
}

GET_POST_LIST_PARAMS = {
    '1.0': [
        ParamsInfo('Type', str, '分区名，填all返回所有分区'),
        ParamsInfo('Limit', str, '帖子条数限制', is_optional=True),
    ],
    '2.0': [
        ParamsInfo('Type', str, '分区名，填all返回所有分区'),
        ParamsInfo('Page', int, '20条帖子为一页，从0开始计数'),
    ]
}

GET_POST_DETAIL_PARAMS = {
    '1.0': [
        ParamsInfo('Pid', str, '帖子序号')
    ],
    '2.0': [
        ParamsInfo('Pid', int, '帖子序号')
    ]
}

SEND_REPLY_PARAMS = {
    '1.0': [
        ParamsInfo('Content', str, '回复内容'),
        ParamsInfo('Pid', str, '被回复帖子序号'),
        ParamsInfo('Author', str, '回复者学号'),
    ],
    '2.0': [
        ParamsInfo('Content', str, '回复内容'),
        ParamsInfo('Pid', int, '被回复帖子序号'),
        ParamsInfo('Author', str, '回复者学号'),
        ParamsInfo('IsAnonymous', bool, '是否匿名，为1则匿名，为0则不匿名'),
    ]
}

GET_REPLY_PARAMS = {
    '1.0': [
        ParamsInfo('Pid', str, '回复所属帖子序号'),
        ParamsInfo('Limit', str, '获取指定条数的回复', is_optional=True),
    ],
    '2.0': [
        ParamsInfo('Pid', str, '回复所属帖子序号'),
        ParamsInfo('Page', int, '获取回复页数，10条回复为一页，从0开始计数'),
    ]
}

DELETE_REPLY_PARAMS = {
    '1.0': [
        ParamsInfo('Rid', int, '回复序号'),
        ParamsInfo('Sid', str, '操作者学号（仅有超级管理员、分区管理员、帖子作者、回复作者可以删除回复）'),
    ]
}

