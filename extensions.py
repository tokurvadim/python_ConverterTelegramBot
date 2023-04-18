import json
import requests
from config import KEYS


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException('неверно введены данные. Вводите данные в формате '
                               '<имя валюты, цену которой Вы хотите узнать> '
                               '<имя валюты, в которой надо узнать цену первой валюты> '
                               '<количество первой валюты>.')
        quote, base, value = values
        if not (quote.lower() in KEYS.keys()):
            raise APIException(
                f"валюта {quote} не найдена. Чтобы отобразить список доступных валют, "
                f"введите команду /values.")
        elif not (base.lower() in KEYS.keys()):
            raise APIException(
                f"валюта {base} не найдена. Чтобы отобразить список доступных валют, "
                f"введите команду /values.")
        if quote == base:
            raise APIException(f'нельзя перевести {quote} в {base}')
        try:
            value = float(value)
        except ValueError:
            raise APIException('не удалось перевести значение валюты в дробный вид. При вводе дробного значения '
                               'валюты используйте точку в качестве разделителя.')
        if value <= 0:
            raise APIException('значение валюты не должно быть меньше 0.')

        base_sign, quote_sign = KEYS.get(base.lower()), KEYS.get(quote.lower())
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_sign}&from={quote_sign}&amount={value}"
        payload = {}
        headers = {
            "apikey": "7bpNPce5cNE3gID0yqNN0TGtExBq0B2D"
        }
        response = requests.get(url, headers=headers, data=payload).content
        result = json.loads(response)
        converting_result = result.get('result')
        return converting_result
