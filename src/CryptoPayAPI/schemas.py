# -*- coding: utf-8 -*-
#
#  CryptoPayAPI - types.
#  Created by LulzLoL231 at 2/6/22
#
import logging
from enum import Enum
from hmac import HMAC
from hashlib import sha256
from decimal import Decimal
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


log = logging.getLogger('CryptoPay')


class Assets(Enum):
    '''Currency code.

    Attributes:
        BTC (str): Bitcoin
        TON (str): Toncoin
        ETH (str): Ethereum
        USDT (str): Tether
        USDC (str): USD Coin
        BUSD (str): Binance USD
    '''
    BTC = 'BTC'
    TON = 'TON'
    ETH = 'ETH'
    USDT = 'USDT'
    USDC = 'USDC'
    BUSD = 'BUSD'

    def __str__(self) -> str:
        return self.value


class PaidButtonNames(Enum):
    '''Name of the button.

    Attributes:
        VIEW_ITEM (str): 'viewItem'
        OPEN_CHANNEL (str): 'openChannel'
        OPEN_BOT (str): 'openBot'
        CALLBACK (str): 'callback'
    '''
    VIEW_ITEM = 'viewItem'
    OPEN_CHANNEL = 'openChannel'
    OPEN_BOT = 'openBot'
    CALLBACK = 'callback'

    def __str__(self) -> str:
        return self.value


class InvoiceStatus(Enum):
    '''Status of invoice.

    Attributes:
        ACTIVE (str): 'active'
        PAID (str): 'paid'
        EXPIRED (str): 'expired'
    '''
    ACTIVE = 'active'
    PAID = 'paid'
    EXPIRED = 'expired'

    def __str__(self) -> str:
        return self.value


class UpdateType(Enum):
    '''Webhook update type.

    Attributes:
        INVOICE_PAID (str): 'invoice_paid
    '''
    INVOICE_PAID = 'invoice_paid'


class Invoice(BaseModel):
    '''Invoice info.

    Attributes:
        invoice_id (int): Unique ID for this invoice.
        status (InvoiceStatus): Status of the invoice.
        hash (str): Hash of the invoice.
        asset (Assets): Currency code.
        amount (Decimal): Amount of the invoice.
        pay_url (str): URL should be presented to the user to pay the invoice.
        description (Optional[str]): *Optional*. Description for this invoice.
        created_at (datetime): Date the invoice was created in ISO 8601 format.
        allow_comments (bool): `True`, if the user can add comment to the payment.
        allow_anonymous (bool): `True`, if the user can pay the invoice anonymously.
        expiration_date (Optional[datetime]): *Optional*. Date the invoice expires in Unix time.
        paid_at (Optional[datetime]): *Optional*. Date the invoice was paid in Unix time.
        paid_anonymously (Optional[bool]): `True`, if the invoice was paid anonymously.
        comment (Optional[str]): *Optional*. Comment to the payment from the user.
        hidden_message (Optional[str]): *Optional*. Text of the hidden message for this invoice.
        payload (Optional[str]): *Optional*. Previously provided data for this invoice.
        paid_btn_name (Optional[PaidButtonNames]): *Optional*. Name of the button.
        paid_btn_url (Optional[str]): *Optional*. URL of the button.
        fee (Optional[Decimal]): *Optional*. Amount of charged service fees. Returned only if the invoice has paid status.
        usd_rate (Optional[Decimal]): *Optional*. Price of the asset in USD. Returned only if the invoice has paid status.
    '''
    invoice_id: int
    status: InvoiceStatus
    hash: str
    asset: Assets
    amount: Decimal
    pay_url: str
    description: Optional[str]
    created_at: datetime
    allow_comments: bool
    allow_anonymous: bool
    expiration_date: Optional[datetime]
    paid_at: Optional[datetime]
    paid_anonymously: Optional[bool]
    comment: Optional[str]
    hidden_message: Optional[str]
    payload: Optional[str]
    paid_btn_name: Optional[PaidButtonNames]
    paid_btn_url: Optional[str]
    fee: Optional[Decimal]
    usd_rate: Optional[Decimal]


class Transfer(BaseModel):
    '''Transfer info.

    Attributes:
        transfer_id (int): Unique ID for this transfer.
        user_id (int): Telegram user ID the transfer was sent to.
        asset (Assets): Currency code.
        amount (Decimal): Amount of the transfer.
        status (Literal['completed']): Status of the transfer, can be “completed”.
        completed_at (datetime): Date the transfer was completed in ISO 8601 format.
        comment (Optional[str]): *Optional*. Comment for this transfer.
    '''
    transfer_id: int
    user_id: int
    asset: Assets
    amount: Decimal
    status: Literal['completed']
    completed_at: datetime
    comment: Optional[str]


class Application(BaseModel):
    '''Application info.

    Attributes:
        app_id (int): Application unique ID.
        name (str): Application name.
        payment_processing_bot_username (str): Username of Crypto bot.
    '''
    app_id: int
    name: str
    payment_processing_bot_username: str


class Balance(BaseModel):
    '''Balance info.

    Attributes:
        currency_code (str): Currency code.
        available (Decimal): Available for using.
    '''
    currency_code: str
    available: Decimal


class ExchangeRate(BaseModel):
    '''Exchange rate info.

    Attributes:
        is_valid (bool): Is valid?
        source (str): Source asset.
        target (str): Target asset.
        rate (Decimal): Exchange rate.
    '''
    is_valid: bool
    source: str
    target: str
    rate: Decimal


class Currency(BaseModel):
    '''Currency info.

    Attributes:
        is_blockchain (bool): Is blockchain asset?
        is_stablecoin (bool): Is stable coin?
        is_fiat (bool): Is fiat asset?
        name (str): Name of currency.
        code (str): Code of currency.
        url (Optional[str]): *Optional*. URL of currency site.
        decimals (int): ?
    '''
    is_blockchain: bool
    is_stablecoin: bool
    is_fiat: bool
    name: str
    code: str
    url: Optional[str]
    decimals: int


class Update(BaseModel):
    '''Webhook update object.

    Attributes:
        update_id (int): Non-unique update ID.
        update_type (UpdateType): Webhook update type.
        request_date (datetime): Date the request was sent in ISO 8601 format.
        payload (Invoice): Payload contains `Invoice` object.
        raw_body (Optional[bytes]): *Optional*. Raw body of update, for check sign purpose.
    '''
    update_id: int
    update_type: UpdateType
    request_date: datetime
    payload: Invoice
    raw_body: Optional[bytes] = None

    def check_signature(self, api_key: str, sign: str) -> bool:
        '''Check update signature.

        Args:
            api_key (str): CryptoPay app API key.
            sign (str): Update signature. In request headers `crypto-pay-api-signature`.

        Returns:
            bool: Is signature verified?
        '''
        log.debug(f'Called with args: ({api_key}, {sign})')
        secret = sha256(api_key.encode()).digest()
        hmac = HMAC(secret, self.raw_body, digestmod=sha256)
        body_sign = hmac.hexdigest()
        log.debug(f'Calculated hash: {body_sign}')
        return body_sign == sign
