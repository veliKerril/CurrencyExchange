# Генерирует выходную информацию для пользователя
class Views:
    ENCODING = 'utf-8'

    # Отправляется при неправильном URL запросе
    @staticmethod
    def create_wrong_request():
        return 'Введен неправильный URL запрос'.encode(encoding=Views.ENCODING)

    ###############################################
    ############## GET запросы ####################
    ###############################################

    # Возвращает представление для /currencies, response 200
    # Принимает на вход json объект
    @staticmethod
    def create_currencies_response200(json_object):
        return json_object.encode(encoding=Views.ENCODING)

    # Возвращает представление для /currencies, response 500
    @staticmethod
    def create_currencies_response500():
        return 'Ошибка на стороне сервера'.encode(encoding=Views.ENCODING)

    # Возвращает представление для /currency/, response 200
    # Принимает на вход json объект
    @staticmethod
    def create_currency_response200(json_object):
        return json_object.encode(encoding=Views.ENCODING)

    # Возвращает представление для /currency/, response 400
    @staticmethod
    def create_currency_response400():
        return 'Неверно введен код валюты'.encode(encoding=Views.ENCODING)

    # Возвращает представление для /currency/, response 404
    @staticmethod
    def create_currency_response404():
        return 'Валюта в базе данных не найдена'.encode(encoding=Views.ENCODING)

    # Возвращает представление для /currency/, response 500
    @staticmethod
    def create_currency_response500():
        return 'Ошибка на стороне сервера'.encode(encoding=Views.ENCODING)

    # Возвращает представление для /exchangeRates, response 200
    # Принимает на вход json объект
    @staticmethod
    def create_exchangeRates_response200(json_object):
        return json_object.encode(encoding=Views.ENCODING)

    # Возвращает представление для /exchangeRates, response 500
    @staticmethod
    def create_exchangeRates_response500():
        return 'Ошибка на стороне сервера'.encode(encoding=Views.ENCODING)

    # Возвращает представление для /exchangeRate/, response 200
    # Принимает на вход json объект
    @staticmethod
    def create_exchangeRate_response200(json_object):
        return json_object.encode(encoding=Views.ENCODING)

    # Возвращает представление для /exchangeRate/, response 400
    @staticmethod
    def create_exchangeRate_response400():
        return 'Коды валют пары отсутствуют в адресе'.encode(encoding=Views.ENCODING)

    # Возвращает представление для /exchangeRate/, response 404
    @staticmethod
    def create_exchangeRate_response404():
        return 'Обменный курс для пары не найден'.encode(encoding=Views.ENCODING)

    # Возвращает представление для /exchangeRate/, response 500
    @staticmethod
    def create_exchangeRate_response500():
        return 'Ошибка на стороне сервера'.encode(encoding=Views.ENCODING)

    # Возвращает представление для /exchange?, response 200
    # Принимает на вход json объект
    @staticmethod
    def create_exchange_response200(json_object):
        return json_object.encode(encoding=Views.ENCODING)

    ###############################################
    ############## POST запросы ###################
    ###############################################

    # Возвращает представление для POST /currencies, response 200
    # Принимает на вход json объект
    @staticmethod
    def create_post_currencies_response200(json_object):
        return json_object.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /currencies, response 400
    @staticmethod
    def create_post_currencies_response400():
        return 'Отсутствует нужное поле формы'.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /currencies, response 409
    @staticmethod
    def create_post_currencies_response409_1():
        return 'Код валюты состоит исключительно из трех латинских букв'.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /currencies, response 409
    @staticmethod
    def create_post_currencies_response409_2():
        return 'Валюта с таким кодом уже существует'.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /currencies, response 500
    @staticmethod
    def create_post_currencies_response500():
        return 'Ошибка на стороне сервера'.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /exchangeRate, response 200
    # Принимает на вход json объект
    @staticmethod
    def create_post_exchangeRate_response200(json_object):
        return json_object.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /exchangeRate, response 400
    @staticmethod
    def create_post_exchangeRate_response400():
        return 'Отсутствует нужное поле формы'.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /exchangeRate, response 400
    @staticmethod
    def create_post_exchangeRate_response404():
        return 'Обменный курс для пары не найден'.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /exchangeRate, response 409
    @staticmethod
    def create_post_exchangeRate_response409():
        return 'Валютная пара с таким кодом уже существует'.encode(encoding=Views.ENCODING)

    # Возвращает представление для POST /exchangeRate, response 500
    @staticmethod
    def create_post_exchangeRate_response500():
        return 'Ошибка на стороне сервера'.encode(encoding=Views.ENCODING)

    ###############################################
    ############## PATCH запросы ##################
    ###############################################

    # Возвращает представление для PATCH /exchangeRate/, response 200
    # Принимает на вход json объект
    @staticmethod
    def create_patch_exchangeRate_response200(json_object):
        return json_object.encode(encoding=Views.ENCODING)

    # Возвращает представление для PATCH /exchangeRate/, response 400
    @staticmethod
    def create_patch_exchangeRate_response400_1():
        return 'Неправильно введены валюты в URL'.encode(encoding=Views.ENCODING)

    # Возвращает представление для PATCH /exchangeRate/, response 400
    @staticmethod
    def create_patch_exchangeRate_response400_2():
        return 'Отсутствует нужное поле формы'.encode(encoding=Views.ENCODING)

    # Возвращает представление для PATCH /exchangeRate/, response 404
    @staticmethod
    def create_patch_exchangeRate_response404():
        return 'Валютная пара отсутствует в базе данных'.encode(encoding=Views.ENCODING)

    # Возвращает представление для PATCH /exchangeRate/, response 500
    @staticmethod
    def create_patch_exchangeRate_response500():
        return 'Ошибка на стороне сервера'.encode(encoding=Views.ENCODING)
