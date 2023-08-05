# a3sdk

## Установка и использование библиотеки

**Установка**

Библиотеку возможно установить при помощи утилиты `pip`:

    pip install A3SDK==0.0.1

**Использование**

```python
from A3SDK import Tokenizer
from A3SDK import PF
```

## Tokenizer

```python
tokenizer = Tokenizer()
tokenizer.is_test = True
```

```python
tokenizer.get_token(
    systemId='EXAMPLE',
    **{
        "systemId": "EXAMPLE",
        "cardNumber": "2200000000000000",
        "cardCVV": "000",
        "cardExp": "1111",
        "cardHolder": "CARD OWNER",
        "orderId": "1"
    })
```

## ProcessingFront

```python
pf = PF()
pf.is_test = True
```

### Method `initPayment`

```python
pf.cancelPayment(
    systemID='EXAMPLE',
    orderID='560ce567-dd57-4d3b-a1b5-d358ce932810'
)
```

### Method `initAuthentication`

```python
...
```

### Method `cancelPayment`

```python
pf.cancelPayment(systemID='EXAMPLE', orderID='560ce567-dd57-4d3b-a1b5-d358ce932810')
```

### Method `enableRecurringKey`

```python
pf.enableRecurringKey(systemID='EXAMPLE', key='1000000000', user={'phone': '9150000000'})
```

```python
{
    'code': 3,
    'description': 'Ключ не найден [key=1000000000].'
}
```


### Method `getPaymentInfo`

```python
pf.getPaymentInfo(**dict(systemID='EXAMPLE', orderID='38d2aefe-21ea-4e3b-91aa-05d9905f2d21'))
```

Примерный ответ

```python
{
    'operationResult': {
        'code': 1,
        'description': 'OK'
    },
    'orderID': '38d2aefe-21ea-4e3b-91aa-05d9905f2d21',
    'authCode': '111111',
    'terminal': '11111111',
    'cardNumber': '220000******0000',
    'bills': None,
    'trID': 1000000000
}
```


### Method `getPaymentStatus`

```python
pf.getPaymentStatus(**dict(systemID='EXAMPLE', orderID='38d2aefe-21ea-4e3b-91aa-05d9905f2d21'))
```

Примерный ответ

```python
{
    'operationResult': {
        'code': 1,
        'description': 'OK'
    },
    'orderStatus': {
        'orderID': '38d2aefe-21ea-4e3b-91aa-05d9905f2d21',
        'trStatus': '2',
        'trStatusDesc': None,
        'trChangeDateTime': None,
        'authCode': '111111',
        'terminal': '11111111',
        'cardNumber': '220000******0000',
        'trID': '1000000000'
    }
}
```


### Method `dailyReportRequest`

```python
pf.dailyReportRequest(
    systemID='EXAMPLE',
    date='2017-08-07',
    status=2,
    signature=''
)
```

Примерный ответ

```python
{
    "operationResult": {
        "code": 3,
        "description": "Неверная подпись."
    },
    "orders": None
}
```