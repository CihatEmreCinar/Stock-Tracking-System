import datetime
from database.db import get_connection
from services import stock_service, cash_service
from database.db import get_connection
from database.models import Sale

def create_sale(barcode, quantity):
    product = stock_service.get_product_by_barcode(barcode)
    if not product:
        raise ValueError("Ürün bulunamadı")
    if product.stock_quantity < quantity:
        raise ValueError("Yeterli stok yok")

    total_price = product.sale_price * quantity * (1 + product.vat_rate / 100)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Sale (product_id, quantity, total_price)
        VALUES (?, ?, ?)
    """, (product.id, quantity, total_price))
    conn.commit()
    conn.close()

    # stok düşür
    stock_service.decrease_stock(product.id, quantity)

    # kasa kaydı
    cash_service.add_income(total_price)

    return total_price

def add_sale(product_id, qty, total_price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO SalesRecord (product_id, qty, total_price, sale_date) VALUES (?, ?, ?, ?)",
        (product_id, qty, total_price, datetime.datetime.now())
    )
    conn.commit()
    conn.close()

def list_sales_by_date(start_date, end_date, limit=50, offset=0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, p.name, s.qty, s.total_price, s.sale_date
        FROM SalesRecord s
        JOIN Product p ON s.product_id = p.id
        WHERE s.sale_date BETWEEN ? AND ?
        ORDER BY s.sale_date DESC
        LIMIT ? OFFSET ?
    """, (start_date, end_date, limit, offset))
    rows = cur.fetchall()
    conn.close()
    return rows