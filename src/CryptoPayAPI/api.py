# -*- coding: utf-8 -*-
#
#  CryptoPayAPI - API.
#  Created by LulzLoL231 at 2/6/22
#
import logging
import urllib.parse
from json import loads
from typing import Dict, Optional, Union, List

from httpx import AsyncClient, Timeout

from . import schemas
from .errors import (
    UnauthorizedError, MethodNotFoundError, UnexpectedError,
    ExpiresInInvalidError, UpdateSignatureError, MethodDisabledError
)


MAINHOST = 'https://pay.crypt.bot/api'
TESTHOST = 'https://testnet-pay.crypt.bot/api'


class CryptoPay:
    '''CryptoPay payment system.
    '''
    def __init__(
        self, api_key: str, testnet: bool = False,
        client: Optional[AsyncClient] = None
    ) -> None:
        '''
        Args:
            api_key (str): CryptoPay API token.
            testnet (bool): Use Testnet? Defaults to False.
            client (AsyncClient, optional): Using custom AsyncClient. Defaults is None.
        '''
        self.timeout_sec = 5
        self.log = logging.getLogger('CryptoPay')
        self.api_key = api_key
        self.headers = {
            'Crypto-Pay-API-Token': api_key
        }
        self.testnet = testnet
        if testnet:
            self.endpoint = TESTHOST
        else:
            self.endpoint = MAINHOST
        self.client = client or AsyncClient(
            headers=self.headers, base_url=self.endpoint,
            timeout=Timeout(self.timeout_sec)
        )

    async def _callApi(self, http_method: str, api_method: str, query: dict = {}) -> dict:
        '''Makes a api call.

        Args:
            http_method (str): HTTP method. Available is "GET" and "POST".
            api_method (str): API method.
            query (dict, optional): Request query in dict. Defaults to {}.

        Returns:
            dict: API response as JSON dict viceversa None.
        '''
        self.log.debug(f'Called with args ({http_method}, {api_method}, {query})')
        if query:
            params = urllib.parse.urlencode(query)
        else:
            params = None
        resp = await self.client.request(http_method, api_method, params=params)
        if resp.is_success:
            data = resp.json()
            self.log.debug(f'API answer: {data}')
            if data['ok']:
                return data['result']
            else:
                raise UnexpectedError(
                    f'[{data["error"]["code"]}] {data["error"]["name"]}',
                    data
                )
        else:
            if resp.status_code == 401:
                raise UnauthorizedError('Token not found!')
            elif resp.status_code == 405:
                raise MethodNotFoundError(
                    f'Method {api_method} not found!'
                )
            elif resp.status_code == 400:
                data = resp.json()
                err = data['error']['name']
                if err == 'EXPIRES_IN_INVALID':
                    raise ExpiresInInvalidError(
                        f'Expires "{query["expires_in"]}" is invalid!',
                        raw_response=data
                    )
            elif resp.status_code == 403:
                data = resp.json()
                err = data['error']['name']
                if err == 'METHOD_DISABLED':
                    raise MethodDisabledError(
                        f'Method "{api_method}" is disabled!',
                        raw_response=data
                    )
            data = resp.json()
            raise UnexpectedError(
                f'[{data["error"]["code"]}] {data["error"]["name"]}',
                raw_response=data
            )

    async def get_me(self) -> schemas.Application:
        '''Returns basic information about an app.

        Returns:
            schemas.Application: Basic information about an app.
        '''
        self.log.debug('Called!')
        result = await self._callApi('GET', 'getMe')
        return schemas.Application(**result)

    async def get_balance(self) -> List[schemas.Balance]:
        '''Use this method to get a balance of your app.

        Returns:
            List[schemas.Balance]: Array of assets.
        '''
        self.log.debug('Called!')
        result = await self._callApi('GET', 'getBalance')
        return [schemas.Balance(**i) for i in result]

    async def get_exchange_rates(self) -> List[schemas.ExchangeRate]:
        '''Use this method to get exchange rates of supported currencies.

        Returns:
            List[schemas.ExchangeRate]: Array of currencies.
        '''
        self.log.debug('Called!')
        result = await self._callApi('GET', 'getExchangeRates')
        return [schemas.ExchangeRate(**i) for i in result]

    async def get_currencies(self) -> List[schemas.Currency]:
        '''Use this method to get a list of supported currencies.

        Returns:
            List[schemas.Currency]: Array of currencies.
        '''
        self.log.debug('Called!')
        result = await self._callApi('GET', 'getCurrencies')
        return [schemas.Currency(**i) for i in result]

    async def create_invoice(self,
                             asset: schemas.Assets,
                             amount: float,
                             description: Optional[str] = None,
                             hidden_message: Optional[str] = None,
                             paid_btn_name: Optional[schemas.PaidButtonNames] = None,
                             paid_btn_url: Optional[str] = None,
                             payload: Optional[str] = None,
                             allow_comments: bool = True,
                             allow_anonymous: bool = True,
                             expires_in: Optional[int] = None) -> schemas.Invoice:
        '''Create a new invoice.

        Args:
            asset (schemas.Assets): Currency.
            amount (float): Amount of invoice in float.
            description (Optional[str]): Description for the invoice. User will see this description when they pay the invoice. Up to 1024 characters. Defaults to None.
            hidden_message (Optional[str]): Text of the message that will be shown to a user after the invoice is paid. Up to 2048 characters. Defaults to None.
            paid_btn_name (Optional[schemas.PaidButtonNames]): Name of the button that will be shown to a user after the invoice is paid. Defaults to None.
            paid_btn_url (Optional[str]): Required if paid_btn_name is used. URL to be opened when the button is pressed. You can set any success link (for example, a link to your bot). Starts with https or http. Defaults to None.
            payload (Optional[str]): Any data you want to attach to the invoice (for example, user ID, payment ID, ect). Up to 4kb. Defaults to None.
            allow_comments (bool): Allow a user to add a comment to the payment. Defaults to True.
            allow_anonymous (bool): Allow a user to pay the invoice anonymously. Defaults to True.
            expires_in (Optional[int]): You can set a payment time limit for the invoice in seconds. Values between 1-2678400 are accepted. Defaults to None.

        Returns:
            schemas.Invoice: Object of the created invoice.
        '''
        self.log.debug(f'Called with args ({asset}, {amount}, {description}, {hidden_message}, {paid_btn_name}, {paid_btn_url}, {payload}, {allow_comments}, {allow_anonymous}, {expires_in})')
        params = {
            'asset': str(asset),
            'amount': amount,
            'allow_comments': allow_comments,
            'allow_anonymous': allow_anonymous
        }
        if description:
            params['description'] = description
        elif hidden_message:
            params['hidden_message'] = hidden_message
        elif paid_btn_name:
            params['paid_btn_name'] = str(paid_btn_name)
            params['paid_btn_url'] = paid_btn_url
        elif payload:
            params['payload'] = payload
        elif expires_in:
            params['expires_in'] = expires_in
        result = await self._callApi('POST', 'createInvoice', params)
        return schemas.Invoice(**result)

    async def get_invoices(self,
                           asset: Optional[schemas.Assets] = None,
                           invoice_ids: Optional[str] = None,
                           status: Optional[schemas.InvoiceStatus] = None,
                           offset: int = 0,
                           count: int = 100) -> List[schemas.Invoice]:
        '''Use this method to get invoices of your app.

        Args:
            asset (Optional[schemas.Assets]): Currency codes separated by comma. Defaults to all assets.
            invoice_ids (Optional[str]): Invoice IDs separated by comma. Defaults to None.
            status (Optional[schemas.InvoiceStatus]): Status of invoices to be returned. Defaults to all statuses.
            offset (int): Offset needed to return a specific subset of invoices. Defaults to 0.
            count (int): Number of invoices to be returned. Values between 1-1000 are accepted. Defaults to 100.

        Returns:
            List[schemas.Invoice]: Array of invoices.
        '''
        self.log.debug(f'Called with args ({asset}, {invoice_ids}, {status}, {offset}, {count})')
        params: Dict[str, Union[str, int]] = {
            'offset': offset,
            'count': count
        }
        if asset:
            params['asset'] = str(asset)
        elif invoice_ids:
            params['invoice_ids'] = invoice_ids
        elif status:
            params['status'] = str(status)
        result = await self._callApi('GET', 'getInvoices', params)
        return [schemas.Invoice(**i) for i in result['items']]

    async def transfer(self,
                       user_id: int,
                       asset: schemas.Assets,
                       amount: float,
                       spend_id: str,
                       comment: Optional[str] = None,
                       disable_send_notification: Optional[bool] = False) -> schemas.Transfer:
        '''Use this method to send coins from your app's balance to a user.

        Args:
            user_id (int): Telegram user_id.
            asset (schemas.Assets): Currency.
            amount (float): Amount of the transfer in float. The minimum and maximum amounts for each of the support asset roughly correspond to the limit of 0.01-25000 USD. Use `get_exchange_rates` to convert amounts.
            spend_id (str): Unique ID to make your request idempotent and ensure that only one of the transfers with the same `spend_id` will be accepted by Crypto Pay API. This parameter is useful when the transfer should be retried (i.e. request timeout, connection reset, 500 HTTP status, etc). It can be some unique withdrawal identifier for example. Up to 64 symbols.
            comment (Optional[str], optional): Comment for the transfer. Users will see this comment when they receive a notification about the transfer. Up to 1024 symbols. Defaults to None.
            disable_send_notification (Optional[bool], optional): Pass `True` if the user should not receive a notification about the transfer. Defaults to False.

        Returns:
            schemas.Transfer: Object of completed `transfer`.
        '''
        self.log.debug(f'Called with args ({user_id}, {asset}, {amount}, {spend_id}, {comment}, {disable_send_notification})')
        params = {
            'user_id': user_id,
            'asset': str(asset),
            'amount': amount,
            'spend_id': spend_id
        }
        if comment:
            params['comment'] = comment
        elif disable_send_notification:
            params['disable_send_notification'] = 'true'
        result = await self._callApi('POST', 'transfer', params)
        return schemas.Transfer(**result)

    async def process_webhook_update(self,
                                     body: bytes,
                                     headers: dict) -> schemas.Update:
        '''Process webhook update.

        Args:
            body (bytes): Update request body.
            headers (dict): Update request headers.

        Returns:
            schemas.Update: Webhook update.
        '''
        self.log.debug(f'Called with args: ({body}, {headers})')  # type: ignore
        update = schemas.Update(**loads(body), raw_body=body)
        sign = headers.get('crypto-pay-api-signature', '')
        if not sign:
            raise UpdateSignatureError(
                'Not found signature!',
                raw_response=update.dict(),
                raw_headers=headers
            )
        if not update.check_signature(self.api_key, sign):
            raise UpdateSignatureError(
                'Signature validation error!',
                raw_response=update.dict(),
                raw_headers=headers
            )
        return update
