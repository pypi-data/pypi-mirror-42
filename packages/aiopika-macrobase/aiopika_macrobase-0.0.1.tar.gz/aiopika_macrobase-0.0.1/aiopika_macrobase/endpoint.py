from enum import Enum

from structlog import get_logger

from macrobase_driver.endpoint import Endpoint

from aio_pika import IncomingMessage, Exchange


log = get_logger('AiopikaEndpoint')


class AiopikaResponseAction(Enum):
    nothing = 0
    ack = 10
    nack = 20
    reject = 30


class AiopikaResponse:

    def __init__(self,
                 action: AiopikaResponseAction,
                 multiple: bool = False,
                 requeue: bool = False,
                 payload: dict = None,
                 *args,
                 **kwargs):
        self.action = action
        self.payload = payload
        self.multiple = multiple
        self.requeue = requeue


class AiopikaEndpoint(Endpoint):

    async def handle(self, exchange: Exchange, message: IncomingMessage, *args, **kwargs):
        return await self.method(exchange, message, *args, **kwargs)

    async def method(self, exchange: Exchange, data=None, *args, **kwargs) -> AiopikaResponse:
        return AiopikaResponse(AiopikaResponseAction.nothing)
