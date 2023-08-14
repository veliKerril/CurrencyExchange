import sqlite3 as sq

with sq.connect('currency_exchange.db') as con:
    cur = con.cursor()
    cur.execute("""
    """)
