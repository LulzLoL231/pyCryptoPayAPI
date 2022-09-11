# -*- coding: utf-8 -*-
#
#  pyCryptoPayAPI - Test testnet connection.
#  Created by LulzLoL231 at 12/9/22
#
from os import environ

import pytest

from CryptoPayAPI import CryptoPay


TOKEN = environ.get('API_TOKEN', '')
APP_NAME = environ.get('APP_NAME', '')
APP_ID = int(environ.get('APP_ID', 0))
if not TOKEN:
    print('Use shell argument "API_TOKEN" for your Crypto Pay API token!')
    exit(1)
if not APP_NAME:
    print('Use shell argument "APP_NAME" for your Crypto Pay app name!')
    exit(1)
if not APP_ID:
    print('Use shell argument "APP_ID" for your Crypto Pay app id!')
    exit(1)


@pytest.mark.asyncio
async def test_testnetconnect():
    cp = CryptoPay(TOKEN, testnet=True)

    app = await cp.get_me()

    assert app.app_id == APP_ID
    assert app.name == APP_NAME

    await cp.client.aclose()
