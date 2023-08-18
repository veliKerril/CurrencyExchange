import sqlite3 as sq
import json

def return_all_cur():
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

        cur.execute("""SELECT * FROM Currencies""")
        data = []
        for elem in cur:
            data.append({})
            data[-1]['id'] = elem[0]
            data[-1]['name'] = elem[1]
            data[-1]['code'] = elem[2]
            data[-1]['sign'] = elem[3]
        return data

"""
В ОБЯЗАТЕЛЬНОМ ПОРЯДКЕ ПОСМОТРЕТЬ ПОСЛЕДНИЕ ДВА УРОКА ПО РАБОТЕ В sql, ЧТОБЫ ПОТОМ ЭТО ПРИМЕНИТЬ
"""
