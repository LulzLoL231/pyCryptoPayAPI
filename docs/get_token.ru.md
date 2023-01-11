# Получение API токена
Для получения CryptoPay API токена, необходимо обратиться к боту [@CryptoBot](https://t.me/CryptoBot).
!!! note "Использование тестовой сети"

    Для получения токена в тестовой сети, обращаться следует к боту [@CryptoTestnetBot](https://t.me/CryptoTestnetBot), и следовать этой инструкции.

## Информация о боте
!!! warning "Проверяйте название бота"

    Перед использованием бота, убедитесь что информация о боте соответствует с указанной ниже!

Для основного бота [@CryptoBot](https://t.me/CryptoBot):  
![main_bot_info](../_images/ru/dark/main_bot_info.png#only-dark){ loading=lazy }
![main_bot_info](../_images/ru/light/main_bot_info.png#only-light){ loading=lazy }

Для тестового бота [@CryptoTestnetBot](https://t.me/CryptoTestnetBot):  
![test_bot_info](../_images/ru/dark/test_bot_info.png#only-dark){ loading=lazy }
![test_bot_info](../_images/ru/light/test_bot_info.png#only-light){ loading=lazy }

## Вход в бота
Используйте команду `/start` в боте для выхода в главное меню и нажмите кнопку <code>🏝️&nbsp;Crypto Pay</code>  
![start](../_images/ru/dark/start.png#only-dark){ loading=lazy }
![start](../_images/ru/light/start.png#only-light){ loading=lazy }

## Создание приложения
Нажмите кнопку <code>Создать&nbsp;приложение</code>, CryptoBot автоматически создаст вам приложение с уникальным именем.  
![cryptopay](../_images/ru/dark/cryptopay.png#only-dark){ loading=lazy }
![cryptopay](../_images/ru/light/cryptopay.png#only-light){ loading=lazy }

## Получение API токена
Нажмите кнопку "API-токен" чтобы увидеть свой API токен, состоит он из идентификатора приложения и уникальной строки в формате `000000:XXXXXXXXXXXXXXXXXXXXXXXXX`  
![app](../_images/ru/dark/app.png#only-dark){ loading=lazy }
![app](../_images/ru/light/app.png#only-light){ loading=lazy }
![token](../_images/ru/dark/token.png#only-dark){ loading=lazy }
![token](../_images/ru/light/token.png#only-light){ loading=lazy }

## Использование токена
Получив токен используйте его при создании инстанса класса [`CryptoPay`][src.CryptoPayAPI.CryptoPay] вот так `CryptoPay('000000:XXXXXXXXXXXXXXXXXXXXXXXXX')`.

!!! warning "Внимание"

    Не забудьте указать флаг `testnet=True` если вы используете токен тестового бота, иначе авторизация не будет пройдена.
