from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
import services.sales_service as sales_service

class SellsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.txtBarcode = QLineEdit()
        self.txtBarcode.setPlaceholderText("Barkod okut")
        self.txtQty = QLineEdit()
        self.txtQty.setPlaceholderText("Adet")

        self.btnSale = QPushButton("Satışı Tamamla")
        self.btnSale.clicked.connect(self.make_sale)

        self.lblResult = QLabel("")

        layout.addWidget(self.txtBarcode)
        layout.addWidget(self.txtQty)
        layout.addWidget(self.btnSale)
        layout.addWidget(self.lblResult)

        self.setLayout(layout)

    def make_sale(self):
        barcode = self.txtBarcode.text()
        qty = int(self.txtQty.text())
        try:
            total = sales_service.create_sale(barcode, qty)
            self.lblResult.setText(f"Satış tamamlandı. Tutar: {total:.2f} TL")
        except Exception as e:
            self.lblResult.setText(str(e))
