import asyncio
from typing import List, Tuple, ClassVar
from functools import partial

from macrobase_driver.driver import MacrobaseDriver

from aiopika_macrobase.config import  AiopikaDriverConfig
from aiopika_macrobase.endpoint import AiopikaResponse, AiopikaResponseAction
from aiopika_macrobase.method import Method
from aiopika_macrobase import exceptions

from structlog import get_logger

import uvloop
import rapidjson
from aio_pika import connect_robust, Connection, IncomingMessage, Exchange, Message


log = get_logger('AiopikaDriver')


class AiopikaDriver(MacrobaseDriver):

    def __init__(self, name: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.config = AiopikaDriverConfig()
        self._connection = None
        self._channel = None
        self._queue = None
        self._methods: List[Method] = []

    def update_config(self, config: AiopikaDriverConfig):
        """
        Add aiopika driver config
        """
        self.config.update(config)

    def add_methods(self, methods: List[Method]):
        self._methods.extend(methods)

    async def decode_message(self, message: IncomingMessage) -> Tuple[str, object]:
        if message.content_type != 'application/json':
            log.error(f'Message {message.correlation_id} have not supported `content_type`')
            raise exceptions.ContentTypeNotSupportedException

        payload = rapidjson.loads(message.body)

        if not isinstance(payload, dict):
            log.error(f'Fail decode body `{str(payload)}`')
            raise exceptions.PayloadFormattingException

        method_name = payload.get('method')

        if method_name is None:
            log.error(f'Fail formatted body `{str(payload)}`')
            raise exceptions.PayloadFormattingException

        log.info(f'Received `{method_name}` method')

        data = payload.get('data')

        return method_name, data

    async def process_message(self, exchange: Exchange, message: IncomingMessage):
        async with message.process(ignore_processed=True):
            log.error(f'Received message {message.correlation_id}')

            response = AiopikaResponse(AiopikaResponseAction.nothing)

            try:
                response = await self._route(exchange, message)
            except exceptions.ContentTypeNotSupportedException as e:
                response = AiopikaResponse(AiopikaResponseAction.reject)
            except exceptions.PayloadFormattingException as e:
                response = AiopikaResponse(AiopikaResponseAction.reject)
            except exceptions.EndpointNotImplementedException as e:
                response = AiopikaResponse(AiopikaResponseAction.reject, requeue=True)
            except exceptions.AiopikaException as e:
                response = AiopikaResponse(AiopikaResponseAction.reject, requeue=True)
            except Exception as e:
                log.error(e)
                response = AiopikaResponse(AiopikaResponseAction.reject, requeue=True)

            if response.action == AiopikaResponseAction.ack:
                if message.reply_to is not None:
                    await self._reply(exchange, message, response.payload)

                await message.ack(multiple=response.multiple)
            elif response.action == AiopikaResponseAction.nack:
                await message.nack(multiple=response.multiple, requeue=response.requeue)
            elif response.action == AiopikaResponseAction.reject:
                await message.reject(requeue=response.requeue)
            else:
                await message.reject(requeue=False)

    async def _route(self, exchange: Exchange, message: IncomingMessage) -> AiopikaResponse:
        method_name, data = await self.decode_message(message)
        method = next((method for method in self._methods if method.name == method_name), None)

        if method is None:
            log.error(f'Message {message.correlation_id} don`t have implemented endpoint')
            raise exceptions.EndpointNotImplementedException

        return await method.handler(exchange, message, data=data)

    async def _reply(self, exchange: Exchange, message: IncomingMessage, payload: dict):
        await exchange.publish(
            Message(
                body=str(rapidjson.dumps(payload)).encode(),
                correlation_id=message.correlation_id
            ),
            routing_key=message.reply_to
        )

    async def _serve(self, loop) -> Connection:
        user            = self.config.RABBITMQ_USER
        password        = self.config.RABBITMQ_PASS
        host            = self.config.RABBITMQ_HOST
        port            = self.config.RABBITMQ_PORT
        virtual_host    = self.config.RABBITMQ_VHOST
        queue           = self.config.RABBITMQ_QUEUE

        connection = await connect_robust(
            host=host,
            port=port,
            login=user,
            password=password,
            virtualhost=virtual_host,

            loop=loop
        )

        self._channel = await connection.channel()
        self._queue = await self._channel.declare_queue(queue)

        await self._queue.consume(
            partial(
                self.process_message,
                self._channel.default_exchange
            )
        )

        return connection

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

        uvloop.install()
        loop = asyncio.get_event_loop()

        connection = loop.run_until_complete(self._serve(loop))

        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(connection.close())
