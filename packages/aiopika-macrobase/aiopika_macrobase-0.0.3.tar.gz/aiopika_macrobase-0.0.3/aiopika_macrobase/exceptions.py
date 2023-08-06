class AiopikaException(Exception):
    pass


class RoutingException(AiopikaException):
    pass


class ContentTypeNotSupportedException(AiopikaException):
    pass


class PayloadFormattingException(AiopikaException):
    pass


class EndpointNotImplementedException(AiopikaException):
    pass
