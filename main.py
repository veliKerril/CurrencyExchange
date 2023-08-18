from http import server
from functools import cached_property
from urllib.parse import parse_qsl, urlparse
from db import return_all_cur
import json


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
        self.wfile.write('Введен неправильный запрос'.encode(encoding='Windows-1251'))

    # Получение списка валют
    # /currencies
    def do_currencies(self):
        self.path = '/currencies'
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        print(return_all_cur())
        # self.wfile.write('Получение списка валют'.encode(encoding='Windows-1251'))
        self.wfile.write(json.dumps(return_all_cur()).encode())

    # Получение конкретной валюты, которая идет после слэша
    # /currency/
    def do_currency(self):
        currency_code = self.url.path[-3:]
        # Валидация на то, что валюта введена корректна и она существует в базе данных
        # if self.url.path[-4] != '/' or ...:
        #     HTTPRequestHandler.wrong_request(self)
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        answer = 'Получение конкретной валюты'.encode(encoding='Windows-1251') + ' '.encode() + currency_code.encode()
        self.wfile.write(answer)

    # Получение списка всех обменных курсов
    # /exchangeRates
    def do_exchange_rates(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Получение списка всех обменных курсов'.encode(encoding='Windows-1251'))

    # Получение конкретного обменного курса
    # /exchangeRate/
    def do_exchange_rates_specific(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Получение конкретного обменного курса'.encode(encoding='Windows-1251'))

    # После вопроса вводятся аргументы и выдается обменный курс
    # /exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT
    # /exchange?from=USD&to=AUD&amount=10
    def do_exchange(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        answer = f'Перевод из {self.query_data["from"]} в {self.query_data["to"]} в количестве {self.query_data["amount"]} штук'
        self.wfile.write(answer.encode(encoding='Windows-1251'))
        # print(self.url)
        # print(self.query_data)

    # Реакция на любой GET запрос
    def do_GET(self):
        if self.path == '/' or self.path == '/currencies':
            HTTPRequestHandler.do_currencies(self)
        elif self.path[:10] == '/currency/':
            HTTPRequestHandler.do_currency(self)
        elif self.path == '/exchangeRates':
            HTTPRequestHandler.do_exchange_rates(self)
        elif self.path[:14] == '/exchangeRate/':
            HTTPRequestHandler.do_exchange_rates_specific(self)
        elif self.path[:9] == '/exchange':
            HTTPRequestHandler.do_exchange(self)
        else:
            HTTPRequestHandler.wrong_request(self)

    def do_post_add_new_currency(self):
        self.send_response(200)
        self.end_headers()

    def do_post_exchange_rate(self):
        self.send_response(200)
        self.end_headers()

    # Реакция на любой POST запрос
    def do_POST(self):
        if self.path == '/currencies':
            HTTPRequestHandler.do_post_add_new_currency(self)
        elif self.path == '/exchangeRates':
            HTTPRequestHandler.do_post_exchange_rate(self)
        else:
            HTTPRequestHandler.wrong_request(self)

    def do_patch_update_exchange_rate(self):
        self.send_response(200)
        self.end_headers()

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