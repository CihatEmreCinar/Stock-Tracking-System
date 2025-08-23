from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
import services.stock_service as stock_service

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
        data = {
            "name": self.txtName.text(),
            "barcode": self.txtBarcode.text(),
            "cost_price": float(self.txtCost.text()),
            "sale_price": float(self.txtSale.text()),
            "vat_rate": float(self.txtVat.text()),
            "stock_quantity": int(self.txtQty.text())
        }
        stock_service.add_product(data)
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
