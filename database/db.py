import sqlite3

DB_NAME = "stok.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Ürünler
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Product(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT UNIQUE,
        name TEXT,
        cost_price REAL,
        sale_price REAL,
        vat_rate REAL,
        stock_quantity INTEGER
    )
    """)

    # Satışlar
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Sale(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        total_price REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Kasa
    cur.execute("""
    CREATE TABLE IF NOT EXISTS CashRecord(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, -- income / expense
        amount REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

from dataclasses import dataclass
