from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
import services.stock_service as stock_service

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
import services.stock_service as stock_service
from utils.barcode import BarcodeScanner  # Barkod okuyucu import edildi

class StockPage(QWidget):
    def __init__(self):
        super().__init__()
        self.scanner = BarcodeScanner()  # Barkod okuyucu örneği

        # UI
        self.txtBarcode = QLineEdit()
        self.txtBarcode.setPlaceholderText("Barkod okut")
        self.btnScan = QPushButton("Barkod Tara")
        self.btnScan.clicked.connect(self.scan_barcode)

        # Diğer alanlar ve tablo tanımları...
    
    def scan_barcode(self):
        try:
            barcode = self.scanner.read_barcode()
            if barcode:
                self.txtBarcode.setText(barcode)
                # İsteğe bağlı: otomatik ürün yükleme
                self.load_product_by_barcode(barcode)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Barkod okuma hatası: {e}")

    def load_product_by_barcode(self, barcode):
        product = stock_service.get_product_by_barcode(barcode)
        if not product:
            QMessageBox.warning(self, "Hata", "Ürün bulunamadı!")
            return
        # Ürün bilgilerini UI'ya yansıt

class StockPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.txtName = QLineEdit()
        self.txtName.setPlaceholderText("Ürün adı")
        self.txtBarcode = QLineEdit()
        self.txtBarcode.setPlaceholderText("Barkod")
        self.txtCost = QLineEdit()
        self.txtCost.setPlaceholderText("Maliyet")
        self.txtSale = QLineEdit()
        self.txtSale.setPlaceholderText("Satış fiyatı")
        self.txtVat = QLineEdit()
        self.txtVat.setPlaceholderText("KDV")
        self.txtQty = QLineEdit()
        self.txtQty.setPlaceholderText("Stok adedi")

        self.btnAdd = QPushButton("Ürün Ekle")
        self.btnAdd.clicked.connect(self.add_product)

        self.table = QTableWidget()
        layout.addWidget(self.txtName)
        layout.addWidget(self.txtBarcode)
        layout.addWidget(self.txtCost)
        layout.addWidget(self.txtSale)
        layout.addWidget(self.txtVat)
        layout.addWidget(self.txtQty)
        layout.addWidget(self.btnAdd)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh_table()

    def add_product(self):
        # Hata kontrolü ve veri doğrulama
        try:
            name = self.txtName.text().strip()
            barcode = self.txtBarcode.text().strip()
            cost_price = float(self.txtCost.text())
            sale_price = float(self.txtSale.text())
            vat_rate = float(self.txtVat.text())
            stock_quantity = int(self.txtQty.text())

            if not name or not barcode:
                raise ValueError("Ürün adı ve barkod boş olamaz.")
            if cost_price < 0 or sale_price < 0 or vat_rate < 0 or stock_quantity < 0:
                raise ValueError("Maliyet, satış fiyatı, KDV ve stok adedi negatif olamaz.")

        except ValueError as ve:
            QMessageBox.warning(self, "Hata", f"Giriş hatası: {ve}")
            return
        except Exception:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doğru formatta doldurun.")
            return

        data = {
            "name": name,
            "barcode": barcode,
            "cost_price": cost_price,
            "sale_price": sale_price,
            "vat_rate": vat_rate,
            "stock_quantity": stock_quantity
        }

        # Mevcut ürün kontrolü
        existing = stock_service.get_product_by_barcode(barcode)
        try:
            if existing:
                stock_service.add_product(data)  # add_product fonksiyonunu stok arttıracak şekilde ayarlamalısın
                QMessageBox.information(self, "Bilgi", f"{existing.name} ürününe {stock_quantity} adet eklendi.")
            else:
                stock_service.add_product(data)
                QMessageBox.information(self, "Bilgi", f"{name} ürünü eklendi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ürün eklenirken bir hata oluştu: {e}")
            return

        # Tabloyu güncelle
        self.refresh_table()

    def refresh_table(self):
        products = stock_service.list_all_products()
        self.table.setRowCount(len(products))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Barkod", "Ad", "Maliyet", "Satış", "Stok"])
        for i, p in enumerate(products):
            self.table.setItem(i, 0, QTableWidgetItem(str(p.id)))
            self.table.setItem(i, 1, QTableWidgetItem(p.barcode))
            self.table.setItem(i, 2, QTableWidgetItem(p.name))
            self.table.setItem(i, 3, QTableWidgetItem(str(p.cost_price)))
            self.table.setItem(i, 4, QTableWidgetItem(str(p.sale_price)))
            self.table.setItem(i, 5, QTableWidgetItem(str(p.stock_quantity)))
