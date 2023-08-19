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
            return json.dumps(data, indent=4)

    # ПОЧТИ ДОПИСАНО, НО НАДО ДОПИСАТЬ!!!
    # ПОЧТИ ДОПИСАНО, НО НАДО ДОПИСАТЬ!!!
    # ПОЧТИ ДОПИСАНО, НО НАДО ДОПИСАТЬ!!!
    # Реагирует на GET для exchangeRates
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
            return data3

    # # ТЕСТОВАЯ ВЕРСИЯ!!!
    # @staticmethod
    #
    #
    # # ТЕСТОВАЯ ВЕРСИЯ!!!
    # @staticmethod
    #
    # # ТЕСТОВАЯ ВЕРСИЯ!!!
    # @staticmethod
    #
    # # ТЕСТОВАЯ ВЕРСИЯ!!!
    # @staticmethod
    #
    # # ТЕСТОВАЯ ВЕРСИЯ!!!
    # @staticmethod


if __name__ == '__main__':
    # print(Model.get_currency('rub'))
    print(Model.get_exchange_rates())