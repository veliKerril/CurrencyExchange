from http import server
from functools import cached_property
from urllib.parse import parse_qsl, urlparse, parse_qs
from model import Model
from views import Views
import my_exceptions


class HTTPRequestHandler(server.BaseHTTPRequestHandler):
    # Парсинг URL
    @cached_property
    def url(self):
        return urlparse(self.path)

    # Запрос с выводом в словарь
    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    # Метод вызывается при обращении по неправильному URL в самом общем виде
    def wrong_request(self):
        self.send_response(400)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.create_wrong_request())

    # Получение списка валют
    # /currencies
    def do_currencies(self):
        self.path = '/currencies'
        try:
            data = Model.get_currencies()
            self.send_response(200)
            self.send_header('content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_currencies_response200(data))
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_currencies_response500())

    # Получение конкретной валюты, которая идет после слэша
    # /currency/
    def do_currency(self):
        currency_code = self.url.path[-3:]
        try:
            if self.url.path[-4] != '/' or not self.url.path[-3:].isalpha():
                raise my_exceptions.CurrencyСodeURL_response400()
            data = Model.get_currency(currency_code)
            self.send_response(200)
            self.send_header('content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_currency_response200(data))
        # Неверно задается код валюты в URL
        except my_exceptions.CurrencyСodeURL_response400:
            self.send_response(400)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_currency_response400())
        # Валюта не находится в базе данных
        except my_exceptions.Currency_response404:
            self.send_response(404)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_currency_response404())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_currency_response500())

    # Получение списка всех обменных курсов
    # /exchangeRates
    def do_exchange_rates(self):
        try:
            data = Model.get_exchange_rates()
            self.send_response(200)
            self.send_header('content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRates_response200(data))
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRates_response500())

    # Получение конкретного обменного курса
    # /exchangeRate/
    def do_exchange_rate(self):
        try:
            if self.url.path[-7] != '/' or not self.url.path[-6:].isalpha():
                raise my_exceptions.CurrencyСodeURL_response400()
            code1 = self.url.path[-6:-3]
            code2 = self.url.path[-3:]
            data = Model.get_exchange_rate(code1, code2)
            self.send_response(200)
            self.send_header('content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRate_response200(data))
        # Неверно задается код валюты в URL
        except my_exceptions.CurrencyСodeURL_response400:
            self.send_response(400)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRate_response400())
        # Не находится обменный курс для пары валют, а пользователь хочет его отобразить
        except my_exceptions.ExchangeRate_response404:
            self.send_response(404)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRate_response404())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRate_response500())

    # После вопроса вводятся аргументы и выдается обменный курс
    # /exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT
    # /exchange?from=USD&to=AUD&amount=10
    def do_exchange(self):
        try:
            data = Model.get_exchange(self.query_data["from"], self.query_data["to"], self.query_data["amount"])
            self.send_response(200)
            self.send_header('content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_exchange_response200(data))
        except:
            HTTPRequestHandler.wrong_request(self)

    # Маппинг GET-запросов
    def do_GET(self):
        if self.path == '/' or self.path == '/currencies':
            HTTPRequestHandler.do_currencies(self)
        elif self.path[:10] == '/currency/':
            HTTPRequestHandler.do_currency(self)
        elif self.path == '/exchangeRates':
            HTTPRequestHandler.do_exchange_rates(self)
        elif self.path[:14] == '/exchangeRate/':
            HTTPRequestHandler.do_exchange_rate(self)
        elif self.path[:9] == '/exchange':
            HTTPRequestHandler.do_exchange(self)
        else:
            HTTPRequestHandler.wrong_request(self)

    # Добавление валюты
    # /currency
    def do_post_add_new_currency(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            answer = parse_qs(str(body)[2:-1])
            if len(answer['code'][0]) != 3 or not answer['code'][0].isalpha():
                raise my_exceptions.PostCurrencies_response409_1()
            data = Model.post_currencies(answer['name'][0], answer['code'][0].upper(), answer['sign'][0])
            self.send_response(200)
            self.send_header('content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_currencies_response200(data))
        # Если выбрасывается KeyError, то значит нет какого-то поля в теле запроса
        except KeyError:
            self.send_response(400)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response400())
        # Пользователь через тело POST-запроса пытается передать невалидный код валют
        except my_exceptions.PostCurrencies_response409_1:
            self.send_response(409)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_currencies_response409_1())
        # Валюта с таким кодом уже существует, а пользователь хочет ее добавить
        except my_exceptions.PostCurrencies_response409:
            self.send_response(409)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_currencies_response409_2())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_currencies_response500())

    # Добавление валютного курса
    # /exchangeRates/
    def do_post_exchange_rate(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            answer = parse_qs(str(body)[2:-1])
            data = Model.post_exchangeRate(answer['baseCurrencyCode'][0], answer['targetCurrencyCode'][0], answer['rate'][0])
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response200(data))
        # Если выбрасывается KeyError, то значит нет какого-то поля в теле запроса
        except KeyError:
            self.send_response(400)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response400())
        # Если нет валютной пары в базе данных или нет хотя бы одной валюты в ней же
        except my_exceptions.ExchangeRate_response404:
            self.send_response(404)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response404())
        # Обменный курс для пары валют существует, а пользователь хочет его добавить
        except my_exceptions.PostExchangeRate_response409:
            self.send_response(409)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response409())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response500())

    # Маппинг POST-запросов
    def do_POST(self):
        if self.path == '/currencies':
            HTTPRequestHandler.do_post_add_new_currency(self)
        elif self.path == '/exchangeRates':
            HTTPRequestHandler.do_post_exchange_rate(self)
        else:
            HTTPRequestHandler.wrong_request(self)

    # Изменение валютного курса
    # /exchangeRate/
    def do_patch_update_exchange_rate(self):
        try:
            if self.url.path[-7] != '/' or not self.url.path[-6:].isalpha():
                raise my_exceptions.CurrencyСodeURL_response400()
            code1 = self.url.path[-6:-3]
            code2 = self.url.path[-3:]
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            rate = parse_qs(str(body)[2:-1])['rate'][0]
            data = Model.patch_exchangeRate(code1, code2, rate)
            self.send_response(200)
            self.send_header('content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response200(data))
        # Если выбрасывается KeyError, то значит нет какого-то поля в теле запроса
        except KeyError:
            self.send_response(400)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response400_2())
        # Неверно задается код валюты в URL
        except my_exceptions.CurrencyСodeURL_response400:
            self.send_response(400)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response400_1())
        # Если нет валютной пары в базе данных или нет хотя бы одной валюты в ней же
        except my_exceptions.ExchangeRate_response404:
            self.send_response(404)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response404())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response500())

    # Маппинг POST-запросов
    def do_PATCH(self):
        if self.path[:14] == '/exchangeRate/':
            HTTPRequestHandler.do_patch_update_exchange_rate(self)
        else:
            HTTPRequestHandler.wrong_request(self)
