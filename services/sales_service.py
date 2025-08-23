from database.db import get_connection
from services import stock_service, cash_service

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
