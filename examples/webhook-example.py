# -*- coding: utf-8 -*-
#
#  pyCryptoPayAPI - webhook example usage.
#  Created by LulzLoL231 at 12/9/22
#
from os import environ

from uvicorn import run
from fastapi import FastAPI, Request

from CryptoPayAPI import CryptoPay


TOKEN = environ.get('CRYPTOPAY_API_TOKEN', '')
if not TOKEN:
    print('Use shell argument "CRYPTOPAY_API_TOKEN" for your Crypto Pay API token!')
    exit(1)


app = FastAPI(
    openapi_tags=None,  # disable docs generating
    redoc_url=None  # disable docs generating
)
cp = CryptoPay(TOKEN)


@app.post('/')
async def process_update(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    update = await cp.process_webhook_update(body, headers)
    print(f'Recieved {update.payload.amount} {update.payload.asset}!')
    return 'ok'


if __name__ == '__main__':
    run(app)
