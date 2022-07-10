from CQU321.register import ParamsInfo

GET_COS_CREDENTIAL_PARAMS = {
    '2.0': [
        ParamsInfo('Type', str, '指定欲进行操作类型，可选download、upload，目前只能访问前缀为"announcements/"的文件')
    ]
}
