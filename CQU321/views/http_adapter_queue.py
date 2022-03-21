"""将 http keep-alive 长连接保存在队列里
"""
from typing import Dict, Type, Union, Tuple, Optional, Container, Mapping, Callable, ContextManager
import logging
from queue import LifoQueue, Empty
import requests
from requests.adapters import BaseAdapter, HTTPAdapter
from requests import adapters, Response, PreparedRequest, Timeout, sessions

_logger = logging.getLogger(__name__)


class QueueBusyException(Timeout):
    def __init__(self) -> None:
        super().__init__("HTTPAdapter queue is busy")


def _http_adapter_ctor() -> HTTPAdapter:
    if hasattr(requests, "hacked_by_queue") and getattr(requests, "hacked_by_queue"):
        return HTTPAdapter(origin=True)
    else:
        return HTTPAdapter()


class HTTPAdapterQueue:
    """:class:`HTTPAdapter` 队列

    :param domains: 进行队列的域名，其中键为 ``协议://域名`` （不包括子域名），
                    如 ``http://cqu.edu.cn``，值为这个 ``协议://域名`` 的队列长度
    :type domains: Dict[str, int]
    :param other: 所有其余域名所在的队列长度，设为 :obj:`None` 则使用新建的 :class:`HTTPAdapter` 而非队列，
                    默认为 :obj:`None`
    :type other: Optional[int], optional
    :param queue_timeout: 最大允许的等待队列的时间（秒），默认为 8
    :type queue_timeout: float, optional
    """

    def __init__(self, domains: Dict[str, int], other: Optional[int] = None, queue_timeout: float = 8):

        self.queue_timeout = queue_timeout

        adapters: Dict[str, LifoQueue[HTTPAdapter]] = {
            domain: LifoQueue(maxsize=num) for domain, num in (domains or {}).items()
        }
        if other:
            adapters["*"] = LifoQueue(maxsize=other)

        for queue in adapters.values():
            for _ in range(queue.maxsize):
                queue.put(_http_adapter_ctor())
        self.adapters: Dict[str, LifoQueue[HTTPAdapter]] = adapters
        adapter_queue = self

        class QueuedAdapter(BaseAdapter):
            def __init__(self) -> None:
                self._http_adapter: Optional[HTTPAdapter] = None
                super().__init__()

            @staticmethod
            def close() -> None:
                pass

            def http_adapter(self) -> HTTPAdapter:
                if not self._http_adapter:
                    self._http_adapter = _http_adapter_ctor()
                return self._http_adapter

            def send(self,
                     request: PreparedRequest,
                     stream: bool = False,
                     timeout: Union[None, float,
                                    Tuple[float, float], Tuple[float, None]] = None,
                     verify: Union[bool, str] = True,
                     cert: Union[None, bytes, str,
                                 Container[Union[bytes, str]]] = None,
                     proxies: Optional[Mapping[str, str]] = None) -> Response:
                with adapter_queue.adapter(request.url, timeout=timeout, adapter_ctor=self.http_adapter) as adapter:
                    return adapter.send(request, stream, timeout, verify, cert, proxies)

        self.adapter_class: Type[BaseAdapter] = QueuedAdapter

    class _QueuedAdapterContext:
        def __init__(self,
                     http_adapter_queue: "HTTPAdapterQueue",
                     url: Optional[str],
                     timeout: Union[None, float, Tuple[float, Optional[float]]],
                     adapter_ctor: Callable[[], HTTPAdapter] = _http_adapter_ctor) -> None:
            if not url:
                return None
            self.domain = '/'.join(url.split('/', maxsplit=4)[:3])
            self.url = url
            self.http_adapter_queue = http_adapter_queue
            self.queue = http_adapter_queue.adapters.get(
                self.domain) or http_adapter_queue.adapters.get("*")
            self.timeout = timeout
            self.adapter_ctor = adapter_ctor
            self.adapter: Optional[HTTPAdapter] = None

        def __enter__(self) -> HTTPAdapter:
            if self.adapter:
                return self.adapter
            if self.queue:
                _logger.debug("Getting adapter from queue of domain %s with %d inside now",
                              self.domain, self.queue.qsize())
                queue_timeout = self.http_adapter_queue.queue_timeout
                if isinstance(self.timeout, (float, int)):
                    queue_timeout = min(self.timeout, queue_timeout)
                elif isinstance(self.timeout, tuple):
                    queue_timeout = min(self.timeout[0], queue_timeout)
                try:
                    self.adapter = self.queue.get(timeout=queue_timeout)
                    _logger.debug(
                        "An adapter of domain %s is gotten with %d left", self.domain, self.queue.qsize())
                    return self.adapter
                except Empty as e:
                    _logger.debug("Adapters of domain %s is busy", self.domain)
                    raise QueueBusyException() from e
            else:
                return self.adapter_ctor()

        def __exit__(self, type, value, traceback) -> None:
            if self.queue:
                if self.adapter:
                    self.queue.put(self.adapter)
                    _logger.debug(
                        "An adapter of domain %s is put back with %d left", self.domain, self.queue.qsize())

    def adapter(self,
                url: Optional[str],
                timeout: Union[None, float,
                               Tuple[float, Optional[float]]] = None,
                adapter_ctor: Callable[[], HTTPAdapter] = HTTPAdapter) -> ContextManager[HTTPAdapter]:
        """获取对应 ``协议://域名`` 的 HTTPAdapter 的一个上下文管理器

        :param url: URL
        :type url: Optional[str]
        :param timeout: 超时设置，和 HTTPAdapter.send 中 timeout 参数格式、含义一致
        :type timeout: Union[None, float, Tuple[float, Optional[float]]]
        :raises QueueBusyException: 队列忙并且超过最大等待时间时抛出
        :return: HTTPAdapter 的上下文管理器
        :rtype: Optional[HTTPAdapter]
        """
        return self._QueuedAdapterContext(self, url, timeout)

    def send(self,
             request: PreparedRequest,
             stream: bool = False,
             timeout: Union[None, float,
                            Tuple[float, float], Tuple[float,  None]] = None,
             verify: Union[bool, str] = True,
             cert: Union[None, bytes, str,
                         Container[Union[bytes, str]]] = None,
             proxies: Optional[Mapping[str, str]] = None) -> Response:
        with self.adapter(request.url, timeout=timeout) as adapter:
            return adapter.send(request, stream, timeout, verify, cert, proxies)

    def patch_requests(self) -> None:
        """给 :module:`requests` 打猴子补丁，默认使用这个队列进行连接

        :return: _description_
        :rtype: _type_
        """
        if not hasattr(requests, "hacked_by_queue"):
            global _http_adapter_origin_new
            HTTPAdapter.__new_backup__ = HTTPAdapter.__new__
            HTTPAdapter.__init_backup__ = HTTPAdapter.__init__

        def hack__new__(cls, *args, **kwargs):
            if kwargs.get("origin"):
                return cls.__new_backup__(cls)
            return self.adapter_class(*args, **kwargs)

        def hack__init__(self, *args, **kwargs):
            if 'origin' in kwargs:
                del kwargs['origin']
            self.__init_backup__(*args, *kwargs)
        requests.hacked_by_queue = True
        HTTPAdapter.__new__ = hack__new__
        HTTPAdapter.__init__ = hack__init__

    @staticmethod
    def unpatch_requests() -> None:
        """取消猴子补丁
        """
        if hasattr(requests, "hacked_by_queue"):
            HTTPAdapter.__new__ = HTTPAdapter.__new_backup__
            HTTPAdapter.__init__ = HTTPAdapter.__init_backup__
            setattr(requests, "hacked_by_queue", False)
