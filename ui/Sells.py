from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, 
    QMessageBox, QTableWidget, QTableWidgetItem, QSpinBox
)
import services.sales_service as sales_service
import services.stock_service as stock_service
from collections import deque

# Sepet ürün yapısı
class CartItem:
    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity

    @property
    def total_price(self):
        kdv = self.product.sale_price * self.quantity * self.product.vat_rate / 100
        return self.product.sale_price * self.quantity + kdv

    @property
    def kdv_amount(self):
        return self.product.sale_price * self.quantity * self.product.vat_rate / 100

# Sepet sınıfı
class ShoppingCart:
    def __init__(self):
        self.items = deque()

    def add_product(self, product, qty=1):
        for item in self.items:
            if item.product.barcode == product.barcode:
                item.quantity += qty
                return
        self.items.append(CartItem(product, qty))

    def remove_product(self, barcode, qty=1):
        for item in self.items:
            if item.product.barcode == barcode:
                item.quantity -= qty
                if item.quantity <= 0:
                    self.items.remove(item)
                return

    def calculate_totals(self):
        total_kdv = sum(item.kdv_amount for item in self.items)
        total_price = sum(item.total_price for item in self.items)
        return total_kdv, total_price

class SellsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.cart = ShoppingCart()

        layout = QVBoxLayout()

        # Barkod Girişi
        self.txtBarcode = QLineEdit()
        self.txtBarcode.setPlaceholderText("Barkod okut")
        self.txtBarcode.returnPressed.connect(self.load_product)
        layout.addWidget(self.txtBarcode)

        # Adet Girişi
        self.txtQty = QLineEdit()
        self.txtQty.setPlaceholderText("Adet")
        layout.addWidget(self.txtQty)

        # Sepet Tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Ürün", "Birim Fiyat", "KDV %", "KDV Tutarı", "Adet", "Toplam"])
        layout.addWidget(self.table)

        # Toplam Alanı
        self.lblKdv = QLabel("Toplam KDV: 0 TL")
        self.lblTotal = QLabel("Toplam Tutar: 0 TL")
        layout.addWidget(self.lblKdv)
        layout.addWidget(self.lblTotal)

        # Satış Butonu
        self.btnSale = QPushButton("Satışı Tamamla")
        self.btnSale.clicked.connect(self.make_sale)
        layout.addWidget(self.btnSale)

        self.setLayout(layout)

    # Ürün ekleme
    def load_product(self):
        barcode = self.txtBarcode.text().strip()
        qty_text = self.txtQty.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Hata", "Lütfen barkod girin.")
            return
        if not qty_text.isdigit() or int(qty_text) <= 0:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir adet girin.")
            return

        product = stock_service.get_product_by_barcode(barcode)
        if not product:
            QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
            return

        self.cart.add_product(product, int(qty_text))
        self.update_table()
        self.txtBarcode.clear()
        self.txtQty.clear()

    # Tablo ve toplam güncelleme
    def update_table(self):
        self.table.setRowCount(len(self.cart.items))
        for row, item in enumerate(self.cart.items):
            self.table.setItem(row, 0, QTableWidgetItem(item.product.name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{item.product.sale_price:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item.product.vat_rate}%"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item.kdv_amount:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(item.quantity)))
            self.table.setItem(row, 5, QTableWidgetItem(f"{item.total_price:.2f}"))

        total_kdv, total_price = self.cart.calculate_totals()
        self.lblKdv.setText(f"Toplam KDV: {total_kdv:.2f} TL")
        self.lblTotal.setText(f"Toplam Tutar: {total_price:.2f} TL")

    # Sepet üzerinden satış
    def make_sale(self):
        if not self.cart.items:
            QMessageBox.warning(self, "Hata", "Sepet boş!")
            return
        try:
            for item in self.cart.items:
                sales_service.create_sale(item.product.barcode, item.quantity)
            QMessageBox.information(self, "Başarılı", "Satış tamamlandı!")
            self.cart = ShoppingCart()
            self.update_table()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Satış sırasında bir hata oluştu: {e}")
