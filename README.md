# pyCryptoPayAPI
![CryptoPay](https://raw.githubusercontent.com/Foile/crypto-pay-api/24a2c869ddc78d12109319c180764ad055fbe687/media/header.svg)

**[Crypto Pay](http://t.me/CryptoBot/?start=pay)** is a payment system based on [@CryptoBot](http://t.me/CryptoBot), which allows you to accept payments in cryptocurrency using the API.

This library help you to work with **Crypto Pay** via [Crypto Pay API](https://help.crypt.bot/crypto-pay-api) in yours Python scripts.

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/LulzLoL231/pyCryptoPayAPI)](https://github.com/LulzLoL231/pyCryptoPayAPI/releases/latest) [![CodeQL](https://github.com/LulzLoL231/pyCryptoPayAPI/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/LulzLoL231/pyCryptoPayAPI/actions/workflows/codeql-analysis.yml) [![Library test](https://github.com/LulzLoL231/pyCryptoPayAPI/actions/workflows/lib-test.yml/badge.svg)](https://github.com/LulzLoL231/pyCryptoPayAPI/actions/workflows/lib-test.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycryptopay-sdk)  
Documentation available on [English language](https://lulzlol231.github.io/pyCryptoPayAPI/en)  
Документация доступна на [Русском языке](https://lulzlol231.github.io/pyCryptoPayAPI/ru)

## Install
Via pip:
```
pip install pycryptopay-sdk
```
Via git:  
```
pip install git+https://github.com/LulzLoL231/pyCryptoPayAPI.git
```
Via source, *in source folder*:  
```
pip install ./
```

## Usage

### API  
First, you need to create your application and get an API token. Open [@CryptoBot](http://t.me/CryptoBot?start=pay) or [@CryptoTestnetBot](http://t.me/CryptoTestnetBot?start=pay) (for testnet), send a command `/pay` to create a new app and get API Token.  
Next step: try to call a simple `get_me()` method to check that everything is working well:

```python
from asyncio import run

from CryptoPayAPI import CryptoPay

cp = CryptoPay('YOUR_API_TOKEN')
print(run(cp.get_me()))  # Returns Application object.
```

You can use `testnet` for testing your applications. Defaults is `mainnet`.

```python
from CryptoPayAPI import CryptoPay

cp = CryptoPay('YOUR_API_TOKEN', testnet=True)
```

You can find all available methods in [Methods chapter](#api-methods).  
Also, you can get supported [assets](#schemasassets), [paid button names](#schemaspaidbuttonnames) and [invoice status](#schemasinvoicestatus):

```python
from asyncio import get_event_loop
from CryptoPayAPI import CryptoPay
from CryptoPayAPI.schemas import Assets, PaidButtonNames, InvoiceStatus


lp = get_event_loop()
cp = CryptoPay('YOUR_API_TOKEN')

print(lp.run_until_complete(cp.create_invoice(
    Assets.USDT, 5.25,
    description='Example page for $5.25!',
    paid_btn_name=PaidButtonNames.VIEW_ITEM,
    paid_btn_url='https://example.com'
)))  # Prints information about created invoice.

print(lp.run_until_complete(cp.get_invoices(
    Assets.USDT, status=InvoiceStatus.PAID
)))  # Prints all paid invoices.
```

### Webhooks
Use Webhooks to get updates for your app, Crypto Pay will send an HTTPS POST request to the specified URL, containing a JSON-serialized [Update](#schemasupdate).  
Read more about webhooks in [Crypto Pay Docs](https://help.crypt.bot/crypto-pay-api#webhooks)!  
Use `CryptoPay.process_webhook_update` function, for processing Crypto Pay requests.  
Check [webhook example](https://github.com/LulzLoL231/pyCryptoPayAPI/tree/main/examples/webhook-example.py) for more info.

#### CryptoPay.process_webhook_update
*Coroutine*. Processing webhook request, returns [Update](#schemasupdate) object.

Arguments:
  * **body** (`bytes`) - JSON content from Crypto Pay request in bytes.
  * **headers** (`dict[str, str]`) - Request headers.
```python
update = await cp.process_webhook_update(body, headers)
print(f'Recieved {update.payload.amount} {update.payload.asset}!')  # Recieved 10.0 ETH
```

Look full code in the [examples](https://github.com/LulzLoL231/pyCryptoPayAPI/tree/main/examples).


## API methods
* [get_me](#get_me)
* [create_invoice](#create_invoice)
* [transfer](#transfer)
* [get_invoices](#get_invoices)
* [get_balances](#get_balances)
* [get_exchange_rates](#get_exchange_rates)
* [get_currencies](#get_currencies)

### get_me
A simple method for testing your app's authentication token. Requires no parameters. Returns basic information about the app.  
Returns: [Application](#schemasapplication) object.

```python
cp.get_me()
```

### create_invoice
Use this method to create a new invoice. Returns object of created invoice.

Arguments:
* **asset** ([Assets](#schemasassets) | `str`) - Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`.
* **amount** (`float`) - Amount of the invoice in float. For example: `125.50`
* **description** (`str`) - *Optional*. Description of the invoice. Up to 1024 symbols.
* **hidden_message** (`str`) - *Optional*. The message will show when the user pays your invoice.
* **paid_btn_name** ([PaidButtonName](#schemaspaidbuttonname) | `str`) - *Optional*. Paid button name. This button will be shown when your invoice was paid. Supported names:

  * `viewItem` - View Item
  * `openChannel` - Open Channel
  * `openBot` - Open Bot
  * `callback` - Return
* **paid_btn_url** (`str`) - *Optional but requried when you use paid_btn_name*. Paid button URL. You can set any payment success link (for example link on your bot). Start with https or http.
* **payload** (`str`, up to 4kb) - *Optional*. Some data. User ID, payment id, or any data you want to attach to the invoice.
* **allow_comments** (`bool`) - *Optional*. Allow adding comments when paying an invoice. Default is True.
* **allow_anonymous** (`bool`) - *Optional*. Allow pay invoice as anonymous. Default is True.
* **expires_in** (`int`) - *Optional*. You can set the expiration date of the invoice in seconds. Use this period: 1-2678400 seconds.

Returns: [Invoice](#schemasinvoice) object of created invoice.

```python
cp.create_invoice(
    Assets.USDT, 5.25,
    description='Example page for $5.25!',
    paid_btn_name=PaidButtonNames.VIEW_ITEM,
    paid_btn_url='https://example.com'
)
```

### transfer
Use this method to send coins from your app to the user. Returns object of completed transfer.

Arguments:
* **user_id** (`int`) - Telegram User ID. The user needs to have an account in our bot (send /start if no).
* **asset** ([Assets](#schemasassets)) - Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`.
* **amount** (`float`) - Amount of the transfer in float. For example: `125.50`
* **spend_id** (`str`) - It is used to make your request idempotent. It's guaranteed that only one of the transfers with the same spend_id will be accepted by Crypto Pay API. This parameter is useful when the transfer should be retried (i.e. request timeout/connection reset/500 HTTP status/etc). You can use a withdrawal id or something. Up to 64 symbols.
* **comment** (`str`) - *Optional*. The comment of the invoice. The comment will show in the notification about the transfer. Up to 1024 symbols.

Returns: [Transfer](#schemastransfer) object of created transfer.

```python
cp.transfer(265300852, Assets.USDT, 3.0, 'pCBA226ghd', comment='donate')
```


### get_invoice
Use this method to get invoices of your app. On success, the returns array of [Invoice](#schemasinvoice).

Arguments:
* **asset** ([Assets](#schemasassets)) - *Optional*. Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`. Default: all assets.
* **invoice_ids** (`str`) - *Optional*. Invoice IDs separated by comma.
* **status** ([InvoiceStatus](#schemasinvoicestatus)) - *Optional*. Status of invoices. Available statuses: active, paid and expired. Default: all statuses.
* **offset** (`int`) - *Optional*. Offset needed to return a specific subset of  invoices. Default 0.
* **count** (`int`) - *Optional*. Number of invoices to return. Default 100, max 1000.

Returns: array of [Invoice](#schemasinvoice) objects.

```python
cp.get_invoices(
    schemas.Assets.USDT, status=schemas.InvoiceStatus.PAID, count=10
)
```

### get_balance
Use this method to get balance of your app. Returns array of assets.

Returns: array of [Balance](#schemasbalance) objects.

```python
cp.get_balance()
```

### get_exchange_rates
Use this method to get exchange rates of supported currencies. Returns array of currencies.

Returns: array of [ExchangeRate](#schemasexchangerate) objects.

```python
cp.get_exchange_rates()
```

### get_currencies
Use this method to supported currencies. Returns array of currencies.

Returns: array of [Currency](#schemascurrency) objects.

```python
cp.get_currencies()
```

## Constants and schemas
```python
from CryptoBotAPI import schemas
```

#### schemas.Asset
constant      | value
------------- | ------
`Assets.BTC`  | `BTC`
`Assets.TON`  | `TON`
`Assets.ETH`  | `ETH`
`Assets.USDT` | `USDT`
`Assets.USDC` | `USDC`
`Assets.BUSD` | `BUSD`

#### schemas.PaidButtonNames
constant                       | value
------------------------------ | -------------
`PaidButtonNames.VIEW_ITEM`    | `viewItem`
`PaidButtonNames.OPEN_CHANNEL` | `openChannel`
`PaidButtonNames.OPEN_BOT`     | `openBot`
`PaidButtonNames.CALLBACK`     | `callback`

#### schemas.InvoiceStatus
constant                | value
----------------------- | ---------
`InvoiceStatus.ACTIVE`  | `active`
`InvoiceStatus.PAID`    | `paid`
`InvoiceStatus.EXPIRED` | `expired`

#### schemas.Invoice
key                | type
------------------ | ------------------------------------
`invoice_id`       | `int`
`status`           | [InvoiceStatus](#schemasinvoicestatus)
`hash`             | `str`
`asset`            | [Assets](#schemasassets)
`amount`           | `decimal.Decimal`
`pay_url`          | `str`
`description`      | `Optional[str]`
`created_at`       | `datetime.datetime`
`allow_comments`   | `bool`
`allow_anonymous`  | `bool`
`expiration_date`  | `Optional[datetime.datetime]`
`paid_at`          | `Optional[datetime.datetime]`
`paid_anonymously` | `Optional[bool]`
`comment`          | `Optional[str]`
`hidden_message`   | `Optional[str]`
`payload`          | `Optional[str]`
`paid_btn_name`    | `Optional[`[PaidButtonNames](#schemaspaidbuttonnames)`]`
`paid_btn_url`     | `Optional[str]`

#### schemas.Transfer
key            | type
-------------- | -----------------------
`transfer_id`  | `int`
`user_id`      | `int`
`asset`        | [Assets](#schemasassets)
`amount`       | `decimal.Decimal`
`status`       | `Literal['completed']`
`completed_at` | `datetime.datetime`
`comment`      | `Optional[str]`

#### schemas.Application
key                               | type
--------------------------------- | -----
`app_id`                          | `int`
`name`                            | `str`
`payment_processing_bot_username` | `str`

#### schemas.Balance
key             | type
--------------- | ------------------
`currency_code` | `str`
`available`     | `decimal.Decimal `

#### schemas.ExchangeRate
key        | type
---------- | -----------------
`is_valid` | `bool`
`source`   | `str`
`target`   | `str`
`rate`     | `decimal.Decimal`

#### schemas.Currency
key             | type
--------------- | ------------------
`is_blockchain` | `bool`
`is_stablecoin` | `bool`
`is_fiat`       | `bool`
`name`          | `str`
`code`          | `str`
`url`           | `Optional[str]`
`decimals`      | `int`

#### schemas.UpdateType
constant                  | value
------------------------- | --------------
`UpdateType.INVOICE_PAID` | `invoice_paid`

#### schemas.Update
key            | type
-------------- | ------------------------------
`update_id`    | `int`
`update_type`  | [UpdateType](#schemasupdatetype)
`request_date` | `datetime`
`payload`      | [Invoice](#schemasinvoice)
