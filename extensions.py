import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        if base == quote:
            raise APIException(f'Невозможно конвертировать одну и ту же валюту "{quote}".\
                                     \nСписок доступных валют: /values')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неверный ввод или несуществующая валюта "{base}".\
                                     \nСписок доступных валют: /values')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Неверный ввод или несуществующая валюта "{quote}".\
                                     \nСписок доступных валют: /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(
                f'Правильно введите число: "{amount}", дробь разделяйте "точкой".')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]

        return total_base
