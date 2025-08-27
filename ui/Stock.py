from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox
)
import services.stock_service as stock_service
from utils.barcode import BarcodeScannerHID  # Barkod okuyucu

class StockPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Form alanları
        self.txtName = QLineEdit()
        self.txtName.setPlaceholderText("Ürün adı")
        self.txtBarcode = QLineEdit()
        self.txtBarcode.setPlaceholderText("Barkod (okut)")
        self.txtCost = QLineEdit()
        self.txtCost.setPlaceholderText("Maliyet")
        self.txtSale = QLineEdit()
        self.txtSale.setPlaceholderText("Satış fiyatı")
        self.txtVat = QLineEdit()
        self.txtVat.setPlaceholderText("KDV")
        self.txtQty = QLineEdit()
        self.txtQty.setPlaceholderText("Stok adedi")

        # Barkod okuyucu (HID) → textbox’a yaz ve onay popup aç
        self.scanner = BarcodeScannerHID(
            self.txtBarcode,
            on_scanned=self.handle_barcode_scanned,
            min_length=3,
            clear_on_scan=False
        )

        # Butonlar
        self.btnAdd = QPushButton("Ürün Ekle")
        self.btnAdd.clicked.connect(self.add_product)

        self.btnUpdate = QPushButton("Ürün Güncelle")
        self.btnUpdate.clicked.connect(self.update_product)

        # Tablo
        self.table = QTableWidget()
        self.table.cellClicked.connect(self.load_selected_product)

        # Layouta ekle
        layout.addWidget(self.txtName)
        layout.addWidget(self.txtBarcode)
        layout.addWidget(self.txtCost)
        layout.addWidget(self.txtSale)
        layout.addWidget(self.txtVat)
        layout.addWidget(self.txtQty)
        layout.addWidget(self.btnAdd)
        layout.addWidget(self.btnUpdate)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh_table()

    # -------------------------------------------------------------------------
    # Barkod ile işlem
    # -------------------------------------------------------------------------
    def handle_barcode_scanned(self, barcode: str):
        """Barkod okutulduğunda popup ile sor ve gerekirse add_product() çalıştır"""
        self.txtBarcode.setText(barcode)

        reply = QMessageBox.question(
            self,
            "Onay",
            f"{barcode} barkodu ile ürünü stoğa eklemek istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.add_product()

    def load_product_by_barcode(self, barcode: str):
        """Barkod okutulunca ürünü bul ve formu doldur"""
        product = stock_service.get_product_by_barcode(barcode)
        if product:
            self.txtBarcode.setText(product.barcode)
            self.txtName.setText(product.name)
            self.txtCost.setText(str(product.cost_price))
            self.txtSale.setText(str(product.sale_price))
            self.txtVat.setText(str(product.vat_rate))
            self.txtQty.setText(str(product.stock_quantity))
        else:
            QMessageBox.warning(self, "Bilgi", f"Barkod bulunamadı: {barcode}")

    # -------------------------------------------------------------------------
    # Tablo işlemleri
    # -------------------------------------------------------------------------
    def load_selected_product(self, row, col):
        """Tablodan seçilen ürünü forma doldur"""
        self.txtBarcode.setText(self.table.item(row, 1).text())
        self.txtName.setText(self.table.item(row, 2).text())
        self.txtCost.setText(self.table.item(row, 3).text())
        self.txtSale.setText(self.table.item(row, 4).text())
        self.txtVat.setText("0")  # tabloya KDV kolonunu ekleyebilirsin
        self.txtQty.setText(self.table.item(row, 5).text())

    def refresh_table(self):
        """Tabloyu güncelle"""
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

    # -------------------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------------------
    def add_product(self):
        """Formdan ürün ekle"""
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
                raise ValueError("Değerler negatif olamaz.")

            data = {
                "name": name,
                "barcode": barcode,
                "cost_price": cost_price,
                "sale_price": sale_price,
                "vat_rate": vat_rate,
                "stock_quantity": stock_quantity
            }

            existing = stock_service.get_product_by_barcode(barcode)
            if existing:
                stock_service.add_product(data)
                QMessageBox.information(self, "Bilgi", f"{existing.name} ürününe {stock_quantity} adet eklendi.")
            else:
                stock_service.add_product(data)
                QMessageBox.information(self, "Bilgi", f"{name} ürünü eklendi.")

            self.refresh_table()

        except ValueError as ve:
            QMessageBox.warning(self, "Hata", f"Giriş hatası: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ürün eklenirken hata: {e}")

    def update_product(self):
        """Seçili ürünü güncelle"""
        try:
            row = self.table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Hata", "Lütfen tabloda bir ürün seçin.")
                return

            product_id = int(self.table.item(row, 0).text())

            data = {
                "name": self.txtName.text().strip(),
                "barcode": self.txtBarcode.text().strip(),
                "cost_price": float(self.txtCost.text()),
                "sale_price": float(self.txtSale.text()),
                "vat_rate": float(self.txtVat.text()),
                "stock_quantity": int(self.txtQty.text())
            }

            stock_service.update_product(product_id, data)
            QMessageBox.information(self, "Bilgi", "Ürün güncellendi.")
            self.refresh_table()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Güncelleme hatası: {e}")
