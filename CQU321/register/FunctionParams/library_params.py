from .. import ParamsInfo

SEARCH_BOOK_PARAMS = {
    '2.0': [
        ParamsInfo('UserName', str, '统一身份认证账号'),
        ParamsInfo('Password', str, '统一身份认证密码'),
        ParamsInfo('Keyword', str, '搜索关键词'),
        ParamsInfo('Page', int, '搜索页数（默认从第一页开始）'),
        ParamsInfo('OnlyHuxi', bool, '为True时，仅检索虎溪图书馆有的书籍')
    ]
}

GET_BOOK_POS_PARAMS = {
    '2.0': [
        ParamsInfo('UserName', str, '统一身份认证账号'),
        ParamsInfo('Password', str, '统一身份认证密码'),
        ParamsInfo('BookId', str, '书籍id'),
    ]
}
