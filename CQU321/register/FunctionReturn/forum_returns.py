from typing import List, Dict

from CQU321.register import ParamsInfo

SEND_POST_RETURNS = {
    '1.0': [],
    '2.0': [],
}

UPDATE_POST_RETURNS = {
    '1.0': [],
    '2.0': [],
}

GET_POST_LIST_RETURNS = {
    '1.0': [
        ParamsInfo('PostList', List, '帖子列表', [
            ParamsInfo('Pid', int, '帖子序号'),
            ParamsInfo('Title', str, '帖子标题'),
            ParamsInfo('Content', str, '帖子内容(仅前14个字)'),
            ParamsInfo('Author', str, '帖子作者'),
            ParamsInfo('Type', str, '帖子类型'),
            ParamsInfo('UserName', str, '作者昵称', can_be_none=True),
            ParamsInfo('UserImg', str, '作者头像', can_be_none=True),
            ParamsInfo('UpdateDate', str, '最后修改时间'),
            ParamsInfo('ReplyNum', int, '帖子回复数量'),
        ])
    ],
    '2.0': [
        ParamsInfo('PostList', List, '帖子列表', [
            ParamsInfo('Pid', int, '帖子序号'),
            ParamsInfo('Title', str, '帖子标题'),
            ParamsInfo('Content', str, '帖子内容(仅前50个字)'),
            ParamsInfo('Author', str, '帖子作者'),
            ParamsInfo('Type', str, '帖子类型'),
            ParamsInfo('UserName', str, '作者昵称', can_be_none=True),
            ParamsInfo('UserImg', str, '作者头像', can_be_none=True),
            ParamsInfo('UpdateDate', str, '最后修改时间'),
            ParamsInfo('ReplyNum', int, '帖子回复数量'),
            ParamsInfo('IsAnonymous', bool, '是否匿名，为1则匿名，为0则不匿名'),
        ])
    ]
}

GET_POST_DETAIL_RETURNS = {
    '1.0': [
        ParamsInfo('PostDetail', Dict, '帖子详情', [
            ParamsInfo('Pid', int, '帖子序号'),
            ParamsInfo('Title', str, '帖子标题'),
            ParamsInfo('Content', str, '帖子内容'),
            ParamsInfo('Author', str, '帖子作者'),
            ParamsInfo('Type', str, '帖子类型'),
            ParamsInfo('UserName', str, '作者昵称', can_be_none=True),
            ParamsInfo('UserImg', str, '作者头像', can_be_none=True),
            ParamsInfo('UpdateDate', str, '最后修改时间'),
            ParamsInfo('Authority', str, '权限'),
        ])
    ],
    '2.0': [
        ParamsInfo('PostDetail', Dict, '帖子详情', [
            ParamsInfo('Title', str, '帖子标题'),
            ParamsInfo('Content', str, '帖子内容'),
            ParamsInfo('Author', str, '帖子作者'),
            ParamsInfo('Type', str, '帖子类型'),
            ParamsInfo('UserName', str, '作者昵称', can_be_none=True),
            ParamsInfo('UserImg', str, '作者头像', can_be_none=True),
            ParamsInfo('UpdateDate', str, '最后修改时间'),
            ParamsInfo('Authority', str, '权限'),
            ParamsInfo('IsAnonymous', bool, '是否匿名，为1则匿名，为0则不匿名'),
        ])
    ]
}

SEND_REPLY_RETURNS = {
    '1.0': [],
    '2.0': [],
}

GET_REPLY_RETURNS = {
    '1.0': [
        ParamsInfo('Reply', List, '回复列表', [
            ParamsInfo('Rid', int, '回复id'),
            ParamsInfo('Content', str, '回复内容'),
            ParamsInfo('Author', str, '回复作者'),
            ParamsInfo('UserName', str, '作者昵称', can_be_none=True),
            ParamsInfo('UserImg', str, '作者头像', can_be_none=True),
            ParamsInfo('UpdateTime', str, '最后修改时间'),
        ])
    ],
    '2.0': [
        ParamsInfo('Reply', List, '回复列表', [
            ParamsInfo('Rid', int, '回复id'),
            ParamsInfo('Content', str, '回复内容'),
            ParamsInfo('Author', str, '回复作者'),
            ParamsInfo('UserName', str, '作者昵称', can_be_none=True),
            ParamsInfo('UserImg', str, '作者头像', can_be_none=True),
            ParamsInfo('UpdateTime', str, '最后修改时间'),
            ParamsInfo('IsAnonymous', bool, '是否匿名，为1则匿名，为0则不匿名'),
        ])
    ],
}

DELETE_REPLY_RETURNS = {
    '1.0': []
}
