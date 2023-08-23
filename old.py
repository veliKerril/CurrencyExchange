# @staticmethod
#     def get_exchange_rate(code1, code2):
        # with sq.connect('CurrencyExchange.db') as con:
        #     cur = con.cursor()
        #     code1 = code1.upper()
        #     code2 = code2.upper()
        #
        #     bool_list = []
        #     cur.execute("""SELECT EXISTS (SELECT Currencies.Code FROM ExchangeRates
        #     JOIN Currencies ON ExchangeRates.BaseCurrencyId = Currencies.ID WHERE Currencies.Code = (?))""", (code1,))
        #     bool_list.append(cur.fetchone()[0])
        #     cur.execute("""SELECT EXISTS (SELECT Currencies.Code FROM ExchangeRates
        #     JOIN Currencies ON ExchangeRates.TargetCurrencyId = Currencies.ID WHERE Currencies.Code = (?))""", (code2,))
        #     bool_list.append(cur.fetchone()[0])
        #
        #     if all(bool_list):
        #         res = []
        #
        #         res.append({})
        #         cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
        #                     FROM ExchangeRates JOIN Currencies ON ExchangeRates.BaseCurrencyId = Currencies.ID
        #                     WHERE Code = (?)""", (code1,))
        #         for elem in cur:
        #             res[-1]['id'] = elem[0]
        #             res[-1]['name'] = elem[1]
        #             res[-1]['code'] = elem[2]
        #             res[-1]['sign'] = elem[3]
        #
        #         res.append({})
        #         cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
        #                     FROM ExchangeRates JOIN Currencies ON ExchangeRates.BaseCurrencyId = Currencies.ID
        #                     WHERE Code = (?)""", (code2,))
        #         for elem in cur:
        #             res[-1]['id'] = elem[0]
        #             res[-1]['name'] = elem[1]
        #             res[-1]['code'] = elem[2]
        #             res[-1]['sign'] = elem[3]
        #         return json.dumps(res, indent=4)
        #     else:
        #         return False

# @staticmethod
# def get_exchange(code1, code2, amount):
#     with sq.connect('CurrencyExchange.db') as con:
#         cur = con.cursor()
#         code1 = code1.upper()
#         code2 = code2.upper()
#
#         cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
#                    FROM ExchangeRates JOIN Currencies ON ExchangeRates.BaseCurrencyId = Currencies.ID""")
#         # Список с кортежами по первой валюте
#         data1 = cur.fetchall()
#         # Запрос, который вытаскивает валюту по второму внешнему ключу
#         cur.execute("""SELECT Currencies.ID,  Currencies.Code, Currencies.FullName, Currencies.Sign
#                                FROM ExchangeRates JOIN Currencies ON ExchangeRates.TargetCurrencyId = Currencies.ID""")
#         # Список с кортежами по второй валюте
#         data2 = cur.fetchall()
#
#         # В эту переменную я вкладываю все возможные пары валют
#         cur_exchange = []
#         code = code1 + code2
#
#         for i in range(len(data1)):
#             cur_exchange.append(str(data1[i][1]))
#             cur_exchange[-1] += str(data2[i][1])
#             if code1 + code2 == cur_exchange[-1] or code2 + code1 == cur_exchange[-1]:
#                 index = i
#                 break
#         set_cur_exchange = set(cur_exchange)
#         # Запрос, который вытаскивает все значения в таблице ExchangeRates
#         cur.execute("""SELECT * FROM ExchangeRates""")
#         data3 = cur.fetchall()
#
#         # Если курс мы можем перевести напрямую
#         if code1 + code2 in set_cur_exchange:
#             rate = data3[index][3]
#             res = {}
#             res['baseCurrency'] = {}
#             res['targetCurrency'] = {}
#             res['baseCurrency']['id'] = data1[index][0]
#             res['baseCurrency']['name'] = data1[index][1]
#             res['baseCurrency']['code'] = data1[index][2]
#             res['baseCurrency']['sign'] = data1[index][3]
#             res['targetCurrency']['id'] = data2[index][0]
#             res['targetCurrency']['name'] = data2[index][1]
#             res['targetCurrency']['code'] = data2[index][2]
#             res['targetCurrency']['sign'] = data2[index][3]
#             res['rate'] = rate
#             res['amount'] = amount
#             res['convertedAmount'] = int(amount) * rate
#             return json.dumps(res, indent=4)
#         # Если надо отработать в обратную сторону
#         elif code2 + code1 in set_cur_exchange:
#             rate = 1 / (data3[index][3] / 1)
#             res = {}
#             res['baseCurrency'] = {}
#             res['targetCurrency'] = {}
#             res['baseCurrency']['id'] = data2[index][0]
#             res['baseCurrency']['name'] = data2[index][1]
#             res['baseCurrency']['code'] = data2[index][2]
#             res['baseCurrency']['sign'] = data2[index][3]
#             res['targetCurrency']['id'] = data1[index][0]
#             res['targetCurrency']['name'] = data1[index][1]
#             res['targetCurrency']['code'] = data1[index][2]
#             res['targetCurrency']['sign'] = data1[index][3]
#             res['rate'] = rate
#             res['amount'] = amount
#             res['convertedAmount'] = int(amount) * rate
#             return json.dumps(res, indent=4)
#         # Если надо посчитать через доллар
#         elif 'USD' + code1 in set_cur_exchange and 'USD' + code2 in set_cur_exchange:
#             index1 = cur_exchange.index('USD' + code1)
#             index2 = cur_exchange.index('USD' + code2)
#             rate1 = data3[index1][3]
#             rate1 = 1 / (rate1 / 1)
#             rate2 = data3[index2][3]
#             rate = rate1 * rate2
#             res = {}
#
#             cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code1,))
#             data = {}
#             for elem in cur:
#                 data['id'] = elem[0]
#                 data['name'] = elem[1]
#                 data['code'] = elem[2]
#                 data['sign'] = elem[3]
#             res['baseCurrency'] = data
#
#             cur.execute("""SELECT * FROM Currencies WHERE Code = (?)""", (code2,))
#             data = {}
#             for elem in cur:
#                 data['id'] = elem[0]
#                 data['name'] = elem[1]
#                 data['code'] = elem[2]
#                 data['sign'] = elem[3]
#             res['targetCurrency'] = data
#
#             res['rate'] = rate
#             res['amount'] = amount
#             res['convertedAmount'] = int(amount) * rate
#             return json.dumps(res, indent=4)
#         # Невозможно сделать перевод
#         else:
#             return json.dumps({'message': 'Not found'}, indent=4)

# +++
# class Response500(Exception):
#     def __init__(self, *args):
#         if args:
#             self.message = args[0]
#         else:
#             self.message = 'Ошибка на стороне сервера'
#
#     def __str__(self):
#         if self.message:
#             return f'response500, {self.message}'
#         else:
#             return 'response500'