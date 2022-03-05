from .. import tools
if tools.config.getboolean("Http_Adapter_Proxy", 'enable'):
    from http_adapter_proxy.client import patch_http_adapter
    patch_http_adapter(tools.config.get("Http_Adapter_Proxy", "socket_path"))
