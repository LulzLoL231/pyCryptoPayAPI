# -*- coding: utf-8 -*-
#
#  CryptoPayAPI - API errors.
#  Created by LulzLoL231 at 2/6/22
#
from typing import Optional


class BaseError(Exception):
    '''Base error class

    Attributes:
        raw_response (dict, optional): RAW response from CryptoPay API.
        raw_headers (dict, optional): RAW headers from CryptoPay API response.
    '''
    def __init__(self,
                 *args: object,
                 raw_response: Optional[dict] = None,
                 raw_headers: Optional[dict] = None) -> None:
        super().__init__(*args)
        self.raw_response = raw_response
        self.raw_headers = raw_headers


class UnauthorizedError(BaseError):
    '''Authorization on CryptoPay API is failed, maybe incorect/expired API token.
    '''
    pass


class MethodNotFoundError(BaseError):
    '''Requested method is not found.
    '''
    pass


class UnexpectedError(BaseError):
    '''Unexpected API error.
    '''
    pass


class ExpiresInInvalidError(BaseError):
    '''Value of `expires_in` is invalid.
    '''
    pass


class UpdateSignatureError(BaseError):
    '''Webhook signature validation error.
    '''
    pass


class MethodDisabledError(BaseError):
    '''Requested method is disabled. Check bot settings.
    '''
    pass
