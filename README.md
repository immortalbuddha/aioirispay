# Aioirispay
Этот проект создан для помощи в автоматизации платежей с помощью ирисок из телеграм-бота Iris; автор не несет никакой ответственности за блокировку ваших аккаунтов в Telegram или в самом боте Iris.


## Установка
Установите библиотеку командой
```sh
pip install aioirispay
```

## Пример использования
Импортируйте библиотеку к себе в проект
```python
from aioirispay import IrisPay
import asyncio

irispay = IrisPay('path/from/session/irispay.session', 'api-id', 'api-hash', 'your-tg-username')

async def main():
    await irispay.start()
    invoice_id = await irispay.create_invoice(amount=1, description='Example')
    target = await irispay.get_user()
    print(f'Передайте кол-во ирисок {target} и укажите комментарий {invoice_id}')

asyncio.run(main())

```

## Разработка

### Требования
Для установки и запуска проекта, необходим [Python](https://python.org/) 3.8+.

## Автор/ы

- [Aleks](tg://resolve?domain=immortalcoder)