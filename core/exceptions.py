from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class AppError(Exception):
    default_code = "app_error"
    default_status = status.HTTP_400_BAD_REQUEST

    def __init__(self, message, code=None, status=None, extra=None):
        self.message = message
        self.code = code or self.default_code
        self.status = status or self.default_status
        self.extra = extra or {}
        super().__init__(message)


class InsufficientFunds(AppError):
    default_code = "insufficient_funds"

class InsufficientShares(AppError):
    default_code = "insufficient_shares"

class SymbolNotFound(AppError):
    default_code = "symbol_not_found"

class MarketDataUnavailable(AppError):
    default_code = "market_data_unavailable"
    default_status = status.HTTP_503_SERVICE_UNAVAILABLE


def api_exception_handler(exc, context):
    if isinstance(exc, AppError):
        return Response(
            {"error": {"code": exc.code, "message": exc.message, **exc.extra}},
            status=exc.status,
        )
    return exception_handler(exc, context)