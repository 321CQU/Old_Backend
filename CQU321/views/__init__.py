from .http_adapter_queue import HTTPAdapterQueue

DEFAULT_DOMAINS = {
    "http://card.cqu.edu.cn": 32,
    "http://authserver.cqu.edu.cn": 32,
    "http://my.cqu.edu.cn": 8,
    "https://my.cqu.edu.cn": 32,
    "http://card.cqu.edu.cn:7280": 32
}
HTTPAdapterQueue(DEFAULT_DOMAINS, other=None).patch_requests()