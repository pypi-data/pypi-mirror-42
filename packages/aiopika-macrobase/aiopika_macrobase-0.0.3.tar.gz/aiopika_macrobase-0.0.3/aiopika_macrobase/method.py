from aiopika_macrobase.endpoint import AiopikaEndpoint
from aiopika_macrobase.exceptions import RoutingException


class Method(object):

    def __init__(self, handler: AiopikaEndpoint, name: str):
        super(Method, self).__init__()

        if not isinstance(handler, AiopikaEndpoint):
            raise RoutingException('Handler must be instance of AiopikaEndpoint class')

        self._handler = handler
        self._name = name

    @property
    def handler(self) -> AiopikaEndpoint:
        return self._handler

    @property
    def name(self) -> str:
        return self._name
