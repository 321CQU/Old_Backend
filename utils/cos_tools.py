import json
from configparser import ConfigParser

from sts.sts import Sts

from Website.settings import BASE_DIR

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/321CQU_Config.ini')


def get_credential(prefix: str = '*', type: str = 'download'):
    if type == 'download':
        actions = [
            "name/cos:GetObject"
        ]
    elif type == 'upload':
        actions = [
            # 简单上传
            'name/cos:PutObject',
            'name/cos:PostObject',
            # 分片上传
            'name/cos:InitiateMultipartUpload',
            'name/cos:ListMultipartUploads',
            'name/cos:ListParts',
            'name/cos:UploadPart',
            'name/cos:CompleteMultipartUpload',
        ]
    elif type == 'test':
        prefix = '*'
        actions = [
            '*'
        ]
    data = {
        'url': 'https://sts.tencentcloudapi.com/',
        # 域名，非必须，默认为 sts.tencentcloudapi.com
        'domain': 'sts.tencentcloudapi.com',
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        'secret_id': config.get('COS', 'secret_id'),
        # 固定密钥
        'secret_key': config.get('COS', 'secret_key'),
        # 换成你的 bucket
        'bucket': '*******',
        # 换成 bucket 所在地区
        'region': '********',
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': prefix,
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': actions
    }

    try:
        sts = Sts(data)
        return sts.get_credential()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(get_credential())
