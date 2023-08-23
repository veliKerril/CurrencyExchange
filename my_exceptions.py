# Вызвается, когда неверно задается код валюты в URL
class CurrencyСodeURL_response400(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Неверно введен код валюты в URL'

    def __str__(self):
        if self.message:
            return f'CurrencyСodeURL_response400, {self.message}'
        else:
            return 'CurrencyСodeURL_response400'


# Вызвается, когда валюта не находится в базе данных
class Currency_response404(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Валюта в базе данных не найдена'

    def __str__(self):
        if self.message:
            return f'Currency_response404, {self.message}'
        else:
            return 'Currency_response404'


# Вызвается, когда не находится обменный курс для пары валют, а пользователь хочет его отобразить
class ExchangeRate_response404(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Обменный курс для пары не найден'

    def __str__(self):
        if self.message:
            return f'ExchangeRate_response404, {self.message}'
        else:
            return 'ExchangeRate_response404'


# Вызвается, когда валюта с таким кодом уже существует, а пользователь хочет ее добавить
class PostCurrencies_response409(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Валюта с таким кодом уже существует'

    def __str__(self):
        if self.message:
            return f'PostCurrencies_response404, {self.message}'
        else:
            return 'PostCurrencies_response404'


# Вызвается, когда обменный курс для пары валют существует, а пользователь хочет его добавить
class PostExchangeRate_response409(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Валютная пара с таким кодом уже существует'

    def __str__(self):
        if self.message:
            return f'PostExchangeRate_response404, {self.message}'
        else:
            return 'PostExchangeRate_response404'


# Вызвается, когда пользователь через тело POST-запроса пытается передать невалидный код валют
class PostCurrencies_response409_1(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Код валюты состоит исключительно из трех латинских букв'

    def __str__(self):
        if self.message:
            return f'PostExchangeRate_response404, {self.message}'
        else:
            return 'PostExchangeRate_response404'
