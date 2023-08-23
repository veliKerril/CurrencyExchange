from http import server
from controller import HTTPRequestHandler

# Запускаем сервер на 80 порту
server = server.HTTPServer(('45.12.239.121', 80), HTTPRequestHandler)
server.serve_forever()
