from http import server
from controller import HTTPRequestHandler

# Запускаем сервер, передаем IP и порт, по которому будем передавать информацию. Вторым аргументом
# вносим класс, который отвечает за обработку http запросов.
server = server.HTTPServer(('87.236.19.5', 8888), HTTPRequestHandler)
server.serve_forever()
