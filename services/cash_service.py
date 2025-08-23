from database.db import get_connection
from database.models import CashRecord

def add_income(amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO CashRecord (type, amount) VALUES (?, ?)", ("income", amount))
    conn.commit()
    conn.close()

def add_expense(amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO CashRecord (type, amount) VALUES (?, ?)", ("expense", amount))
    conn.commit()
    conn.close()

def get_balance():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) FROM CashRecord")
    balance = cur.fetchone()[0] or 0
    conn.close()
    return balance
