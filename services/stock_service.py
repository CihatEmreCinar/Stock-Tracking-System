from database.db import get_connection
from database.models import Product
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# ...existing code...



def add_product(data):
    existing = get_product_by_barcode(data["barcode"])
    conn = get_connection()
    cur = conn.cursor()
    
    if existing:
        # Mevcut ürün varsa stok adedini arttır
        cur.execute(
            "UPDATE Product SET stock_quantity = stock_quantity + ? WHERE id = ?",
            (data["stock_quantity"], existing.id)
        )
    else:
        # Yeni ürün ekle
        cur.execute("""
            INSERT INTO Product (barcode, name, cost_price, sale_price, vat_rate, stock_quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["barcode"], data["name"], data["cost_price"],
            data["sale_price"], data["vat_rate"], data["stock_quantity"]
        ))
    
    conn.commit()
    conn.close()

from database.models import Product  # dataclass için

def update_product(product_id: int, data: dict):
    """Ürün bilgilerini güncelle (sqlite3)"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Product
        SET name = ?, barcode = ?, cost_price = ?, sale_price = ?, vat_rate = ?, stock_quantity = ?
        WHERE id = ?
    """, (
        data["name"],
        data["barcode"],
        data["cost_price"],
        data["sale_price"],
        data["vat_rate"],
        data["stock_quantity"],
        product_id
    ))

    conn.commit()
    conn.close()



def list_all_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Product")
    rows = cur.fetchall()
    conn.close()
    return [Product(*row) for row in rows]

def get_product_by_barcode(barcode):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Product WHERE barcode=?", (barcode,))
    row = cur.fetchone()
    conn.close()
    return Product(*row) if row else None

def decrease_stock(product_id, qty):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Product SET stock_quantity = stock_quantity - ? WHERE id=?", (qty, product_id))
    conn.commit()
    conn.close()
