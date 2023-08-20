from http import server
from functools import cached_property
from urllib.parse import parse_qsl, urlparse, parse_qs
from model import Model
from views import Views


class MyException1(Exception):
    pass


class MyException2(Exception):
    pass


class MyException3(Exception):
    pass

# Хендлер - это обработчик http запросов,
# То есть я наследуюсь от базового хендлера, и теперь могу обрабатывать http запросы
class HTTPRequestHandler(server.BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    # Запрос с выводом в словарь
    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    """
    Две функции ниже - пока что непонятный для меня функционал, однако он может быть крайне полезным
    Они связаны уже POST, это попозже сделаем
    """
    @cached_property
    def post_data(self):
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode('utf-8')))

    # Функция при обращении по неправильному URL в самом общем виде
    def wrong_request(self):
        self.send_response(400)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(Views.create_wrong_request())

    # Получение списка валют
    # Почти доделанная функция - остается решить только вопрос с кодировкой знаков
    # /currencies
    def do_currencies(self):
        self.path = '/currencies'
        # Кодировку знаков доделать, все остальное хорошо
        try:
            data = Model.get_currencies()
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_currencies_response200(data))
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_currencies_response500())

    # Получение конкретной валюты, которая идет после слэша
    # Почти доделанная функция - остается нормально проверить введенные валюты и прописать эксепшены
    # /currency/
    def do_currency(self):
        currency_code = self.url.path[-3:]
        try:
            if self.url.path[-4] != '/' or not self.url.path[-3:].isalpha():
                raise MyException1
            data = Model.get_currency(currency_code)
            # Почему-то пустой json объект имеет длину два
            if not data:
                raise MyException2
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_currency_response200(data))
        except MyException1:
            self.send_response(400)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_currency_response400())
        except MyException2:
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_currency_response404())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_currency_response500())

    # Получение списка всех обменных курсов
    # Почти доделанная функция - остается не всю информацию вытаскивать в оперативную память
    # /exchangeRates
    def do_exchange_rates(self):
        try:
            data = Model.get_exchange_rates()
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRates_response200(data))
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRates_response500())

    # Получение конкретного обменного курса
    # /exchangeRate/
    def do_exchange_rate(self):
        try:
            if self.url.path[-7] != '/' or not self.url.path[-6:].isalpha():
                raise MyException1
            code1 = self.url.path[-6:-3]
            code2 = self.url.path[-3:]
            data = Model.get_exchange_rate(code1, code2)
            if not data:
                raise MyException2
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRate_response200(data))
        except MyException1:
            self.send_response(400)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRate_response400())
        except MyException2:
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRate_response404())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_exchangeRate_response500())

    # После вопроса вводятся аргументы и выдается обменный курс
    # /exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT
    # /exchange?from=USD&to=AUD&amount=10
    # Тестовая реализация 2
    def do_exchange(self):
        try:
            data = Model.get_exchange(self.query_data["from"], self.query_data["to"], self.query_data["amount"])
            # Не смогли перевести
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_exchange_response200(data))
        except:
            HTTPRequestHandler.wrong_request(self)

    # Реакция на любой GET запрос
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

    # Тестовая версия 3
    def do_post_add_new_currency(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            answer = parse_qs(str(body)[2:-1])
            data = Model.post_currencies(answer['name'][0], answer['code'][0], answer['sign'][0])
            bool1 = False
            bool2 = False
            if bool1:
                raise MyException1
            # Почему-то пустой json объект имеет длину два
            if bool2:
                raise MyException2
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_post_currencies_response200(data))
        except MyException1:
            self.send_response(400)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response400())
        except MyException2:
            self.send_response(409)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_post_currencies_response409())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_post_currencies_response400())

    def do_post_exchange_rate(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            answer = parse_qs(str(body)[2:-1])
            data = Model.post_exchangeRate(answer['baseCurrencyCode'][0], answer['targetCurrencyCode'][0], answer['rate'][0])
            bool1 = False
            bool2 = False
            if bool1:
                raise MyException1
            # Почему-то пустой json объект имеет длину два
            if bool2:
                raise MyException2
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response200(data))
        except MyException1:
            self.send_response(400)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response400())
        except MyException2:
            self.send_response(409)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response409())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_post_exchangeRate_response500())

    # Реакция на любой POST запрос
    def do_POST(self):
        if self.path == '/currencies':
            HTTPRequestHandler.do_post_add_new_currency(self)
        elif self.path == '/exchangeRates':
            HTTPRequestHandler.do_post_exchange_rate(self)
        else:
            HTTPRequestHandler.wrong_request(self)

    def do_patch_update_exchange_rate(self):
        try:
            if self.url.path[-7] != '/' or not self.url.path[-6:].isalpha():
                raise MyException1
            code1 = self.url.path[-6:-3]
            code2 = self.url.path[-3:]
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            rate = parse_qs(str(body)[2:-1])['rate'][0]
            data = Model.patch_exchangeRate(code1, code2, rate)
            bool2 = False
            # Почему-то пустой json объект имеет длину два
            if bool2:
                raise MyException2
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response200(data))
        except MyException1:
            self.send_response(400)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response400())
        except MyException2:
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response404())
        except:
            self.send_response(500)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(Views.create_patch_exchangeRate_response500())

    # Реакция на любой PATCH запрос
    def do_PATCH(self):
        if self.path[:14] == '/exchangeRate/':
            HTTPRequestHandler.do_patch_update_exchange_rate(self)
        else:
            HTTPRequestHandler.wrong_request(self)


# Запускаем сервер, передаем IP и порт, по которому будем передавать информацию. Вторым аргументом
# вносим класс, который отвечает за обработку http запросов.
server = server.HTTPServer(('localhost', 8000), HTTPRequestHandler)
server.serve_forever()
