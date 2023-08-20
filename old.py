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