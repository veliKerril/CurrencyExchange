import sqlite3 as sq
import json

'''
В обязательном порядке переписать комментарии
'''

class Model:
    # Метод, который обнуляет базу данных и создает ее с нуля, заполняя тестовыми начальными значениями
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
            # ВОЗМОЖНО, ЕСТЬ СМЫСЛ ИНФОРМАЦИЮ ВЫНЕСТИ В ОТДЕЛЬНЫЕ КОРТЕЖИ
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

    # Метод, который возвращает все доступные валюты в виде JSON
    @staticmethod
    def get_currencies():
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM Currencies""")
            data = []
            for elem in cur:
                data.append({})
                data[-1]['id'] = elem[0]
                data[-1]['name'] = elem[1]
                data[-1]['code'] = elem[2]
                data[-1]['sign'] = elem[3]
            return json.dumps(data, indent=4)

    # Метод, который возвращает конкретную валюты по коду в виде JSON
    @staticmethod
    def get_currency(code):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            code = code.upper()
            cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code,))
            data = {}
            for elem in cur:
                data['id'] = elem[0]
                data['name'] = elem[1]
                data['code'] = elem[2]
                data['sign'] = elem[3]
            if data:
                return json.dumps(data, indent=4)
            else:
                return False

    # Полный треш - я всю информацию загружаю в питон и тут анализирую
    # Реагирует на GET для /exchangeRates
    @staticmethod
    def get_exchange_rates():
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            # Запрос, который вытаскивает валюту по первому внешнему ключу
            cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
            FROM ExchangeRates JOIN Currencies ON ExchangeRates.BaseCurrencyId = Currencies.ID""")
            # Список с кортежами по первой валюте
            data1 = cur.fetchall()
            # Запрос, который вытаскивает валюту по второму внешнему ключу
            cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
                        FROM ExchangeRates JOIN Currencies ON ExchangeRates.TargetCurrencyId = Currencies.ID""")
            # Список с кортежами по второй валюте
            data2 = cur.fetchall()
            # Запрос, который вытаскивает все значения в таблице ExchangeRates
            cur.execute("""SELECT * FROM ExchangeRates""")
            data3 = cur.fetchall()
            res = []
            for i in range(len(data3)):
                res.append({})
                res[-1]['id'] = data3[i][0]
                res[-1]['baseCurrency'] = {}
                res[-1]['targetCurrency'] = {}
                res[-1]['rate'] = data3[i][3]
                res[-1]['baseCurrency']['id'] = data1[i][0]
                res[-1]['baseCurrency']['name'] = data1[i][1]
                res[-1]['baseCurrency']['code'] = data1[i][2]
                res[-1]['baseCurrency']['sign'] = data1[i][3]
                res[-1]['targetCurrency']['id'] = data2[i][0]
                res[-1]['targetCurrency']['name'] = data2[i][1]
                res[-1]['targetCurrency']['code'] = data2[i][2]
                res[-1]['targetCurrency']['sign'] = data2[i][3]
            return json.dumps(res, indent=4)

    # Полный треш - я всю информацию загружаю в питон и тут анализирую
    # Реагирует на GET для /exchangeRate/, то есть выдает конкретную валютную пару
    @staticmethod
    def get_exchange_rate(code1, code2):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            code1 = code1.upper()
            code2 = code2.upper()

            cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
                       FROM ExchangeRates JOIN Currencies ON ExchangeRates.BaseCurrencyId = Currencies.ID""")
            # Список с кортежами по первой валюте
            data1 = cur.fetchall()
            # Запрос, который вытаскивает валюту по второму внешнему ключу
            cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
                                   FROM ExchangeRates JOIN Currencies ON ExchangeRates.TargetCurrencyId = Currencies.ID""")
            # Список с кортежами по второй валюте
            data2 = cur.fetchall()

            # В эту переменную я вкладываю все возможные пары валют
            cur_exchange = []
            code = code1 + code2

            for i in range(len(data1)):
                cur_exchange.append(str(data1[i][1]))
                cur_exchange[-1] += str(data2[i][1])
                if code == cur_exchange[-1]:
                    index = i
                    break
            set_cur_exchange = set(cur_exchange)

            if code not in set_cur_exchange:
                return False
            else:
                # Запрос, который вытаскивает все значения в таблице ExchangeRates
                cur.execute("""SELECT * FROM ExchangeRates""")
                data3 = cur.fetchall()
                res = {}
                res['id'] = data3[index][0]
                res['baseCurrency'] = {}
                res['targetCurrency'] = {}
                res['rate'] = data3[index][3]
                res['baseCurrency']['id'] = data1[index][0]
                res['baseCurrency']['name'] = data1[index][1]
                res['baseCurrency']['code'] = data1[index][2]
                res['baseCurrency']['sign'] = data1[index][3]
                res['targetCurrency']['id'] = data2[index][0]
                res['targetCurrency']['name'] = data2[index][1]
                res['targetCurrency']['code'] = data2[index][2]
                res['targetCurrency']['sign'] = data2[index][3]
                return json.dumps(res, indent=4)

    # Полный треш, совсем плохо - полностью переписывать логику
    # Реагирует на GET для /exchange?
    @staticmethod
    def get_exchange(code1, code2, amount):
        with sq.connect('CurrencyExchange.db') as con:
            cur = con.cursor()
            code1 = code1.upper()
            code2 = code2.upper()

            cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
                       FROM ExchangeRates JOIN Currencies ON ExchangeRates.BaseCurrencyId = Currencies.ID""")
            # Список с кортежами по первой валюте
            data1 = cur.fetchall()
            # Запрос, который вытаскивает валюту по второму внешнему ключу
            cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
                                   FROM ExchangeRates JOIN Currencies ON ExchangeRates.TargetCurrencyId = Currencies.ID""")
            # Список с кортежами по второй валюте
            data2 = cur.fetchall()

            # В эту переменную я вкладываю все возможные пары валют
            cur_exchange = []
            code = code1 + code2

            for i in range(len(data1)):
                cur_exchange.append(str(data1[i][1]))
                cur_exchange[-1] += str(data2[i][1])
                if code1+code2 == cur_exchange[-1] or code2+code1 == cur_exchange[-1]:
                    index = i
                    break
            set_cur_exchange = set(cur_exchange)
            # Запрос, который вытаскивает все значения в таблице ExchangeRates
            cur.execute("""SELECT * FROM ExchangeRates""")
            data3 = cur.fetchall()

            # Если курс мы можем перевести напрямую
            if code1+code2 in set_cur_exchange:
                rate = data3[index][3]
                res = {}
                res['baseCurrency'] = {}
                res['targetCurrency'] = {}
                res['baseCurrency']['id'] = data1[index][0]
                res['baseCurrency']['name'] = data1[index][1]
                res['baseCurrency']['code'] = data1[index][2]
                res['baseCurrency']['sign'] = data1[index][3]
                res['targetCurrency']['id'] = data2[index][0]
                res['targetCurrency']['name'] = data2[index][1]
                res['targetCurrency']['code'] = data2[index][2]
                res['targetCurrency']['sign'] = data2[index][3]
                res['rate'] = rate
                res['amount'] = amount
                res['convertedAmount'] = int(amount) * rate
                return json.dumps(res, indent=4)
            # Если надо отработать в обратную сторону
            elif code2+code1 in set_cur_exchange:
                rate = 1 / (data3[index][3] / 1)
                res = {}
                res['baseCurrency'] = {}
                res['targetCurrency'] = {}
                res['baseCurrency']['id'] = data2[index][0]
                res['baseCurrency']['name'] = data2[index][1]
                res['baseCurrency']['code'] = data2[index][2]
                res['baseCurrency']['sign'] = data2[index][3]
                res['targetCurrency']['id'] = data1[index][0]
                res['targetCurrency']['name'] = data1[index][1]
                res['targetCurrency']['code'] = data1[index][2]
                res['targetCurrency']['sign'] = data1[index][3]
                res['rate'] = rate
                res['amount'] = amount
                res['convertedAmount'] = int(amount) * rate
                return json.dumps(res, indent=4)
            # Если надо посчитать через доллар
            elif 'USD'+code1 in set_cur_exchange and 'USD'+code2 in set_cur_exchange:
                index1 = cur_exchange.index('USD'+code1)
                index2 = cur_exchange.index('USD'+code2)
                rate1 = data3[index1][3]
                rate1 = 1 / (rate1 / 1)
                rate2 = data3[index2][3]
                rate = rate1 * rate2
                res = {}

                cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code1,))
                data = {}
                for elem in cur:
                    data['id'] = elem[0]
                    data['name'] = elem[1]
                    data['code'] = elem[2]
                    data['sign'] = elem[3]
                res['baseCurrency'] = data

                cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code2,))
                data = {}
                for elem in cur:
                    data['id'] = elem[0]
                    data['name'] = elem[1]
                    data['code'] = elem[2]
                    data['sign'] = elem[3]
                res['targetCurrency'] = data

                res['rate'] = rate
                res['amount'] = amount
                res['convertedAmount'] = int(amount) * rate
                return json.dumps(res, indent=4)
            # Невозможно сделать перевод
            else:
                return json.dumps({'message': 'Not found'}, indent=4)

    # ТЕСТОВАЯ ВЕРСИЯ!!! 3
    
    @staticmethod
    def post_currencies(name, code, sign):
        return json.dumps({'name': name, 'code': code, 'sign': sign}, indent=4)

    # ТЕСТОВАЯ ВЕРСИЯ!!! 4
    @staticmethod
    def post_exchangeRate(baseCurrencyCode, targetCurrencyCode, rate):
        return json.dumps({'baseCurrencyCode': baseCurrencyCode, 'targetCurrencyCode': targetCurrencyCode,\
                           'rate': rate}, indent=4)

    # ТЕСТОВАЯ ВЕРСИЯ!!! 5
    @staticmethod
    def patch_exchangeRate(code1, code2, rate):
        test = json.dumps({'code1': code1, 'code2': code2, 'rate': rate}, indent=4)
        return test


if __name__ == '__main__':
    # print(Model.get_currency('rub'))
    print(Model.get_exchange('rub', 'aud', 10))
