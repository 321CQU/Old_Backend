from typing import List, Dict

from .. import ParamsInfo

SEARCH_BOOK_RETURNS = {
    '2.0': [
        ParamsInfo('SearchSet', List, '查询结果集', [
            ParamsInfo('BookId', str, '书籍编号'),
            ParamsInfo('Title', str, '书籍标题'),
            ParamsInfo('ImgUrl', str, '书籍封面地址（为默认封面时为None）', can_be_none=True),
            ParamsInfo('Publisher', str, '出版社'),
            ParamsInfo('Year', str, '出版年份'),
            ParamsInfo('Authors', List, '书籍作者列表', sub_params=[
                ParamsInfo('Author', str, '作者名称', name_is_key=False)
            ]),
            ParamsInfo('Introduction', str, '书籍简介'),
            ParamsInfo('Pos', List, '藏书地点列表', sub_params=[
                ParamsInfo('LibraryName', str, '图书馆名称'),
                ParamsInfo('LibraryPosition', str, '藏书地点'),
                ParamsInfo('BookSearchId', str, '索书号'),
                ParamsInfo('Statue', str, '书籍状态（在馆/已借出）')
            ])
        ])
    ]
}

GET_BOOK_POS_RETURNS = {
    '2.0': [
        ParamsInfo('Pos', List, '藏书地点列表', sub_params=[
            ParamsInfo('LibraryName', str, '图书馆名称'),
            ParamsInfo('LibraryPosition', str, '藏书地点'),
            ParamsInfo('BookSearchId', str, '索书号'),
            ParamsInfo('Statue', str, '书籍状态（在馆/已借出）')
        ])
    ]
}
