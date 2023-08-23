import sqlite3 as sq
import json
import my_exceptions


class Model:
    # При запуске метода база данных откатывается до первоначальных тестовых значений.
    # При отстутствии базы данных она создается
    @staticmethod
    def reset_and_create_bd():
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()

            # Удаляю и создаю таблицу с информацией о валютах
            cur.execute("""DROP TABLE IF EXISTS Currencies""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Currencies (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Code TEXT UNIQUE NOT NULL,
            FullName TEXT NOT NULL,
            Sign TEXT NOT NULL
            )""")

            # Заполняю ее тестовыми значениями
            # Возможно, есть смысл информацию вынести в отдельные кортежи
            cur.execute("""INSERT INTO Currencies VALUES (1, 'USD', 'US Dollar', '$')""")
            cur.execute("""INSERT INTO Currencies VALUES (2, 'EUR', 'Euro', '€')""")
            cur.execute("""INSERT INTO Currencies VALUES (3, 'JPY', 'Yen', '¥')""")
            cur.execute("""INSERT INTO Currencies VALUES (4, 'GBP', 'Pound Sterling', '£')""")
            cur.execute("""INSERT INTO Currencies VALUES (5, 'AUD', 'Australian Dollar', 'A$')""")
            cur.execute("""INSERT INTO Currencies VALUES (6, 'RUB', 'Russian Ruble', '₽')""")

            # Удаляю и создаю заново вторую таблицу с курсом обмена
            cur.execute("""DROP TABLE IF EXISTS ExchangeRates""")
            cur.execute("""CREATE TABLE IF NOT EXISTS ExchangeRates (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            BaseCurrencyId INTEGER,
            TargetCurrencyId INTEGER,
            Rate REAL NOT NULL,
            FOREIGN KEY(BaseCurrencyId) REFERENCES Currencies(ID),
            FOREIGN KEY(TargetCurrencyId) REFERENCES Currencies(ID)
            )""")

            # Заполняю ее тестовыми значениями
            cur.execute("""INSERT INTO ExchangeRates VALUES (1, 6, 1, 0.011)""")
            cur.execute("""INSERT INTO ExchangeRates VALUES (2, 6, 2, 0.0097)""")
            cur.execute("""INSERT INTO ExchangeRates VALUES (3, 6, 3, 1.53)""")
            cur.execute("""INSERT INTO ExchangeRates VALUES (4, 6, 4, 0.0082)""")
            cur.execute("""INSERT INTO ExchangeRates VALUES (5, 6, 5, 0.016)""")
            cur.execute("""INSERT INTO ExchangeRates VALUES (6, 1, 2, 0.92)""")
            cur.execute("""INSERT INTO ExchangeRates VALUES (7, 1, 3, 145.16)""")
            cur.execute("""INSERT INTO ExchangeRates VALUES (8, 1, 4, 0.78)""")
            cur.execute("""INSERT INTO ExchangeRates VALUES (9, 1, 6, 95.20)""")

    # Возвращает все доступные валюты в виде JSON
    @staticmethod
    def get_currencies():
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM Currencies""")
            data = []
            for elem in cur:
                data.append({})
                data[-1]['id'] = elem[0]
                data[-1]['name'] = elem[2]
                data[-1]['code'] = elem[1]
                data[-1]['sign'] = elem[3]
            return json.dumps(data, indent=4)

    # Возвращает конкретную валюту по коду в виде JSON
    @staticmethod
    def get_currency(code):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            code = code.upper()
            cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code,))
            currency = cur.fetchone()
            # Вызываю исключение, если валюта не находится в базе данных
            if not currency:
                raise my_exceptions.Currency_response404()
            data = {'id': currency[0], 'name': currency[1], 'code': currency[2], 'sign': currency[3]}
            return json.dumps(data, indent=4)

    # Возвращает все обменные курсы в виде JSON
    @staticmethod
    def get_exchange_rates():
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()

            cur.execute("""SELECT * FROM ExchangeRates""")
            data = cur.fetchall()
            res = []
            for i in range(len(data)):
                res.append({})
                res[-1]['id'] = data[i][0]
                res[-1]['baseCurrency'] = {}
                res[-1]['targetCurrency'] = {}
                res[-1]['rate'] = data[i][3]
                cur.execute("""SELECT * FROM Currencies WHERE ID = (?)""", (data[i][1],))
                data1 = cur.fetchone()
                res[-1]['baseCurrency']['id'] = data1[0]
                res[-1]['baseCurrency']['name'] = data1[2]
                res[-1]['baseCurrency']['code'] = data1[1]
                res[-1]['baseCurrency']['sign'] = data1[3]
                cur.execute("""SELECT * FROM Currencies WHERE ID = (?)""", (data[i][2],))
                data2 = cur.fetchone()
                res[-1]['targetCurrency']['id'] = data2[0]
                res[-1]['targetCurrency']['name'] = data2[2]
                res[-1]['targetCurrency']['code'] = data2[1]
                res[-1]['targetCurrency']['sign'] = data2[3]
            return json.dumps(res, indent=4)

    # Выдает конкретную валютную пару
    @staticmethod
    def get_exchange_rate(code1, code2):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            code1 = code1.upper()
            code2 = code2.upper()

            cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code1,))
            data1 = cur.fetchone()
            cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code2,))
            data2 = cur.fetchone()

            # Если одной из валют нет в базе данных
            if not data1 or not data2:
                raise my_exceptions.ExchangeRate_response404()

            id1 = data1[0]
            id2 = data2[0]

            # Проверка на наличие валютной пары в базе данных
            cur.execute("""SELECT COUNT(ID) FROM ExchangeRates WHERE BaseCurrencyId = (?)
                            AND TargetCurrencyId = (?)""", (id1, id2))
            count_of_pair = cur.fetchone()[0]

            # Если не находится обменный курс для пары валют, а пользователь хочет его отобразить
            if count_of_pair == 0:
                raise my_exceptions.ExchangeRate_response404()

            # Запрос, который вытаскивает нужную строку из обмена
            cur.execute("""SELECT * FROM ExchangeRates WHERE BaseCurrencyId = (?)
                            AND TargetCurrencyId = (?)""", (id1, id2))
            data3 = cur.fetchone()
            res = {}
            res['id'] = data3[0]
            res['baseCurrency'] = {}
            res['targetCurrency'] = {}
            res['rate'] = data3[3]
            res['baseCurrency']['id'] = data1[0]
            res['baseCurrency']['name'] = data1[1]
            res['baseCurrency']['code'] = data1[2]
            res['baseCurrency']['sign'] = data1[3]
            res['targetCurrency']['id'] = data2[0]
            res['targetCurrency']['name'] = data2[1]
            res['targetCurrency']['code'] = data2[2]
            res['targetCurrency']['sign'] = data2[3]
            return json.dumps(res, indent=4)

    # Реагирует на GET для /exchange?
    # /exchange?from=USD&to=AUD&amount=10
    @staticmethod
    def get_exchange(code1, code2, amount):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            code1 = code1.upper()
            code2 = code2.upper()

            cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code1,))
            data1 = cur.fetchone()
            id1 = data1[0]
            cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code2,))
            data2 = cur.fetchone()
            id2 = data2[0]

            cur.execute("""SELECT ID FROM Currencies WHERE Code = 'USD'""")
            id_usd = cur.fetchone()[0]

            # Проверка на наличие валютной пары в базе данных
            cur.execute("""SELECT COUNT(ID) FROM ExchangeRates WHERE BaseCurrencyId = (?) AND TargetCurrencyId = (?)""", (id1, id2))
            case1 = cur.fetchone()[0]
            cur.execute("""SELECT COUNT(ID) FROM ExchangeRates WHERE BaseCurrencyId = (?) AND TargetCurrencyId = (?)""", (id2, id1))
            case2 = cur.fetchone()[0]
            cur.execute("""SELECT COUNT(ID) FROM ExchangeRates WHERE BaseCurrencyId = (?) AND TargetCurrencyId = (?)""", (id_usd, id1))
            case3 = cur.fetchone()[0]
            cur.execute("""SELECT COUNT(ID) FROM ExchangeRates WHERE BaseCurrencyId = (?) AND TargetCurrencyId = (?)""", (id_usd, id2))
            case4 = cur.fetchone()[0]

            # Если курс мы можем перевести напрямую
            if case1:
                cur.execute("""SELECT Rate FROM ExchangeRates WHERE BaseCurrencyId = (?) AND TargetCurrencyId = (?)""", (id1, id2))
                rate = cur.fetchone()[0]
                res = {}
                res['baseCurrency'] = {}
                res['targetCurrency'] = {}
                res['baseCurrency']['id'] = data1[0]
                res['baseCurrency']['name'] = data1[2]
                res['baseCurrency']['code'] = data1[1]
                res['baseCurrency']['sign'] = data1[3]
                res['targetCurrency']['id'] = data2[0]
                res['targetCurrency']['name'] = data2[2]
                res['targetCurrency']['code'] = data2[1]
                res['targetCurrency']['sign'] = data2[3]
                res['rate'] = rate
                res['amount'] = amount
                res['convertedAmount'] = round(int(amount) * rate, 6)
                return json.dumps(res, indent=4)
            # Если надо отработать в обратную сторону
            elif case2:
                cur.execute("""SELECT Rate FROM ExchangeRates WHERE BaseCurrencyId = (?) AND TargetCurrencyId = (?)""", (id2, id1))
                rate_first = cur.fetchone()[0]
                rate = 1 / (rate_first / 1)
                res = {}
                res['baseCurrency'] = {}
                res['targetCurrency'] = {}
                res['baseCurrency']['id'] = data2[0]
                res['baseCurrency']['name'] = data2[2]
                res['baseCurrency']['code'] = data2[1]
                res['baseCurrency']['sign'] = data2[3]
                res['targetCurrency']['id'] = data1[0]
                res['targetCurrency']['name'] = data1[2]
                res['targetCurrency']['code'] = data1[1]
                res['targetCurrency']['sign'] = data1[3]
                res['rate'] = rate
                res['amount'] = amount
                res['convertedAmount'] = round(int(amount) * rate, 6)
                return json.dumps(res, indent=4)
            # Если надо посчитать через доллар
            elif case3 and case4:
                cur.execute("""SELECT Rate FROM ExchangeRates WHERE BaseCurrencyId = (?) AND TargetCurrencyId = (?)""", (id_usd, id1))
                rate1 = cur.fetchone()[0]
                cur.execute("""SELECT Rate FROM ExchangeRates WHERE BaseCurrencyId = (?) AND TargetCurrencyId = (?)""", (id_usd, id2))
                rate2 = cur.fetchone()[0]
                rate1 = 1 / (rate1 / 1)
                rate = round(rate1 * rate2, 6)
                res = {}
                data = {}
                data['id'] = data1[0]
                data['name'] = data1[2]
                data['code'] = data1[1]
                data['sign'] = data1[3]
                res['baseCurrency'] = data
                data = {}
                data['id'] = data2[0]
                data['name'] = data2[2]
                data['code'] = data2[1]
                data['sign'] = data2[3]
                res['targetCurrency'] = data

                res['rate'] = rate
                res['amount'] = amount
                res['convertedAmount'] = round(int(amount) * rate, 6)
                return json.dumps(res, indent=4)
            # В случае какой-либо ошибки с этой функцией
            else:
                return json.dumps({'message': 'Not found'}, indent=4)

    # Добавляет новую валюту в базу данных
    @staticmethod
    def post_currencies(name, code, sign):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()

            # Делаем проверку на существовании валюты в базе данных
            cur.execute("""SELECT COUNT(Code) FROM Currencies WHERE Code = (?)""", (code,))
            if cur.fetchone()[0] > 0:
                raise my_exceptions.PostCurrencies_response409()

            cur.execute("""INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)""", (code, name, sign))

        return json.dumps({'name': name, 'code': code, 'sign': sign}, indent=4)

    # Добавляет новый обменный курс
    @staticmethod
    def post_exchangeRate(code1, code2, rate):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            code1 = code1.upper()
            code2 = code2.upper()
            rate = round(float(rate), 6)

            # Вытаскиваем ID первой и второй валюты
            cur.execute("""SELECT ID FROM Currencies WHERE Currencies.Code = (?)""", (code1,))
            data1 = cur.fetchone()
            cur.execute("""SELECT ID FROM Currencies WHERE Currencies.Code = (?)""", (code2,))
            data2 = cur.fetchone()

            # Если хотя бы одной валюты нет в базе данных, то вызывается исключение
            if not data1 or not data2:
                raise my_exceptions.ExchangeRate_response404()

            id1 = cur.fetchone()[0]
            id2 = cur.fetchone()[0]

            # Проверка на наличие валютной пары в базе данных
            cur.execute("""SELECT COUNT(ID) FROM ExchangeRates WHERE BaseCurrencyId = (?)
                            AND TargetCurrencyId = (?)""", (id1, id2))
            if cur.fetchone()[0] == 1:
                raise my_exceptions.PostExchangeRate_response409()

            cur.execute("""INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate)
                            VALUES (?, ?, ?)""", (id1, id2, rate))

            return json.dumps({'baseCurrencyCode': code1, 'targetCurrencyCode': code2,\
                               'rate': rate}, indent=4)

    # Изменяет валютный курс пары
    @staticmethod
    def patch_exchangeRate(code1, code2, rate):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            code1 = code1.upper()
            code2 = code2.upper()
            rate = round(float(rate), 6)

            cur.execute("""SELECT ID FROM Currencies WHERE Currencies.Code = (?)""", (code1, ))
            data1 = cur.fetchone()
            cur.execute("""SELECT ID FROM Currencies WHERE Currencies.Code = (?)""", (code2,))
            data2 = cur.fetchone()

            # Вызвается исключение, если хотя бы одной валюты не существует в базе данных
            if not data1 or not data2:
                raise my_exceptions.ExchangeRate_response404()

            id1 = cur.fetchone()[0]
            id2 = cur.fetchone()[0]

            # Проверка на наличие валютной пары в базе данных
            cur.execute("""SELECT COUNT(ID) FROM ExchangeRates WHERE BaseCurrencyId = (?)
                        AND TargetCurrencyId = (?)""", (id1, id2))
            if cur.fetchone()[0] == 0:
                raise my_exceptions.ExchangeRate_response404()

            cur.execute("""UPDATE ExchangeRates SET Rate = (?) WHERE BaseCurrencyId = (?)
                        AND TargetCurrencyId = (?)""", (rate, id1, id2))

            return json.dumps({'code1': code1, 'code2': code2, 'rate': rate}, indent=4)
