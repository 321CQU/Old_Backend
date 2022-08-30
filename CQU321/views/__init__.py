from ..utils.http_adapter_queue import HTTPAdapterQueue
# import logging
#
# logging.basicConfig(level=logging.DEBUG)

DEFAULT_DOMAINS = {
    "http://card.cqu.edu.cn": 32,
    "http://authserver.cqu.edu.cn": 32,
    "http://my.cqu.edu.cn": 8,
    "https://my.cqu.edu.cn": 32,
    "http://card.cqu.edu.cn:7280": 32
}
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36 Edge/40.15254.603'
HTTPAdapterQueue(DEFAULT_DOMAINS, other=None,
                 default_user_agent=DEFAULT_USER_AGENT).patch_requests()
