import datetime
from database.db import get_connection
from services import stock_service, cash_service

def create_sale(barcode, quantity):
    product = stock_service.get_product_by_barcode(barcode)
    if not product:
        raise ValueError("Ürün bulunamadı")
    if product.stock_quantity < quantity:
        raise ValueError("Yeterli stok yok")

    vat_amount = product.sale_price * quantity * (product.vat_rate / 100)
    total_price = product.sale_price * quantity + vat_amount

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Sale (product_id, quantity, total_price, date, vat_amount)
        VALUES (?, ?, ?, ?, ?)
    """, (product.id, quantity, total_price, datetime.datetime.now(), vat_amount))
    conn.commit()
    conn.close()

    # stok düşür
    stock_service.decrease_stock(product.id, quantity)

    # kasa kaydı
    cash_service.add_income(total_price)

    return total_price


def add_sale(product_id, quantity, total_price, vat_amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Sale (product_id, quantity, total_price, date, vat_amount) VALUES (?, ?, ?, ?, ?)",
        (product_id, quantity, total_price, datetime.datetime.now(), vat_amount)
    )
    conn.commit()
    conn.close()


def list_sales_by_date(start_date, end_date, limit=50, offset=0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, 
               p.name, 
               s.quantity, 
               s.total_price, 
               s.date, 
               s.vat_amount AS kdv_amount
        FROM Sale s
        JOIN Product p ON s.product_id = p.id
        WHERE s.date BETWEEN ? AND ?
        ORDER BY s.date DESC
        LIMIT ? OFFSET ?
    """, (start_date, end_date, limit, offset))
    rows = cur.fetchall()
    conn.close()
    return rows
