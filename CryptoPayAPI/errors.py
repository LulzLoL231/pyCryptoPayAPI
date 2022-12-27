# -*- coding: utf-8 -*-
#
#  CryptoPayAPI - API errors.
#  Created by LulzLoL231 at 2/6/22
#
from typing import Optional


class BaseError(Exception):
    def __init__(self,
                 *args: object,
                 raw_response: Optional[dict] = None,
                 raw_headers: Optional[dict] = None) -> None:
        super().__init__(*args)
        self.raw_response = raw_response
        self.raw_headers = raw_headers


class UnauthorizedError(BaseError):
    pass


class MethodNotFoundError(BaseError):
    pass


class UnexpectedError(BaseError):
    pass


class ExpiresInInvalidError(BaseError):
    pass


class UpdateSignatureError(BaseError):
    pass


class MethodDisabledError(BaseError):
    pass
