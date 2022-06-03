class NotSendException(Exception):
    """Исключение не для пересылки в Telegram"""
    pass


class RequestError(NotSendException):
    """Отсутствует подключение к API"""


class EmptyResponseError(NotSendException):
    """Пустой запрос"""
    pass


class HTTPStatusError(NotSendException):
    """Пришел статус отличный от 200"""
    pass


class TokenError(NotSendException):
    """Отсутствует одна из переменных окружения"""
    pass
