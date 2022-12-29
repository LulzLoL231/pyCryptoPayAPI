# Get API token
To get a CryptoPay API token, you need to contact the bot [@CryptoBot](https://t.me/CryptoBot).
!!! note "Using the testnet"

    To get a token in the test network, you should contact the bot [@CryptoTestnetBot](https://t.me/CryptoTestnetBot), and follow this instruction.

## About bot
!!! warning "Check bot name"

    Before using the bot, make sure that the information about the bot matches the one below!

For main bot [@CryptoBot](https://t.me/CryptoBot):  
![main_bot_info](../_images/en/dark/main_bot_info.png#only-dark){ loading=lazy }
![main_bot_info](../_images/en/light/main_bot_info.png#only-light){ loading=lazy }

from test bot [@CryptoTestnetBot](https://t.me/CryptoTestnetBot):  
![test_bot_info](../_images/en/dark/test_bot_info.png#only-dark){ loading=lazy }
![test_bot_info](../_images/en/light/test_bot_info.png#only-light){ loading=lazy }

## Start bot
Use the `/start` command in the bot to exit to the main menu and press the button <code>🏝️&nbsp;Crypto Pay</code>  
![start](../_images/en/dark/start.png#only-dark){ loading=lazy }
![start](../_images/en/light/start.png#only-light){ loading=lazy }

## Creating of application
Click the <code>Create&nbsp;application</code> button, CryptoBot will automatically create an application for you with a unique name.  
![cryptopay](../_images/en/dark/cryptopay.png#only-dark){ loading=lazy }
![cryptopay](../_images/en/light/cryptopay.png#only-light){ loading=lazy }

## Getting API token
Click the "API token" button to see your API token, it consists of an application identifier and a unique string in the format `000000:XXXXXXXXXXXXXXXXXXXXXXXXX`  
![app](../_images/en/dark/app.png#only-dark){ loading=lazy }
![app](../_images/en/light/app.png#only-light){ loading=lazy }
![token](../_images/en/dark/token.png#only-dark){ loading=lazy }
![token](../_images/en/light/token.png#only-light){ loading=lazy }

## Using of token
After receiving the token, use it when creating an instance of the class [`CryptoPay`][src.CryptoPayAPI.CryptoPay] like this `CryptoPay('000000:XXXXXXXXXXXXXXXXXXXXXXXXX')`.

!!! warning

    Don't forget to set the `testnet=True` flag if you are using a test bot token, otherwise authorization will fail.
