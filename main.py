import sqlite3 as sq
from http import server
from functools import cached_property
from urllib.parse import parse_qsl, urlparse
'''
Я пока что не понимаю, что и как мне делать, поэтому весь код буду писать здесь
'''

with sq.connect('currency_exchange.db') as con:
    cur = con.cursor()
    cur.execute("""
    """)


# Хендлер - это обработчик http запросов,
# То есть я наследуюсь от базового хендлера, и теперь по кайфу могу обрабатывать http запросы
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
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    def wrong_request(self):
        """
        Тут, по сути, клиент не прав и обратился по несуществующей странице
        """
        self.send_response(400)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Введен неправильный запрос'.encode(encoding="Windows-1251"))

    # Получение списка валют
    def do_currencies(self):
        self.path = '/currencies'
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Получение списка валют'.encode(encoding="Windows-1251"))

    # Получение конкретной валюты, которая идет после слэша
    def do_currency(self):
        currency_code = self.url.path[-3:]
        # Валидация на то, что валюта введена корректна и она существует в базе данных
        # if self.url.path[-4] != '/' or ...:
        #     HTTPRequestHandler.wrong_request(self)
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Получение конкретной валюты'.encode(encoding="Windows-1251") + ' ' + currency_code.encode())

    # Получение списка всех обменных курсов
    def do_exchange_rates(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Получение списка всех обменных курсов'.encode(encoding="Windows-1251"))

    def do_exchange_rates_specific(self):
        """
        После еще одного слеша - получение конкретного обменного курса
        """
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        # self.wfile.write(b'Получение списка всех обменных курсов')
        self.wfile.write(b'222')


    def do_exchange(self):
        """
        Тут после слова через вопрос должны выдаваться все необходимые значения
        """
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        # self.wfile.write(b'Расчёт перевода определённого количества средств из одной валюты в другую.')
        self.wfile.write(b'3')
        print(self.url)
        print(self.query_data)
        print(self.post_data)
        print(self.form_data)

    # Тут я показываю, как реагировать на запросы типа GET
    # Не совсем понятно, где мы рассматриваем адрес
    def do_GET(self):
        if self.path == '/' or self.path == '/currencies':
            HTTPRequestHandler.do_currencies(self)
        elif self.path[:10] == '/currency/':
            HTTPRequestHandler.do_currency(self)
        elif self.path == '/exchangeRates':
            HTTPRequestHandler.do_exchange_rates(self)
        elif self.path[:15] == '/exchangeRates/':
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

    def do_PATCH(self):
        if self.path[:14] == '/exchangeRate/':
            HTTPRequestHandler.do_patch_update_exchange_rate(self)
        else:
            HTTPRequestHandler.wrong_request(self)


# Запускаем сервер, передаем IP и порт, по которому будем передавать информацию. Вторым аргументом
# вносим класс, который отвечает за обработку http запросов.
server = server.HTTPServer(('localhost', 8000), HTTPRequestHandler)
server.serve_forever()