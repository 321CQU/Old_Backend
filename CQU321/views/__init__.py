from .. import tools
if tools.config.getboolean("HTTP_ADAPTER", 'enable'):
    from http_adapter_proxy.client import patch_http_adapter
    patch_http_adapter(tools.config.get("HTTP_ADAPTER", "socket_path"))
