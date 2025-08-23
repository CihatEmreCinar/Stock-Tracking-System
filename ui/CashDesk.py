from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import services.cash_service as cash_service

class CashDeskPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.lblBalance = QLabel()
        layout.addWidget(self.lblBalance)

        self.setLayout(layout)
        self.refresh_balance()

    def refresh_balance(self):
        balance = cash_service.get_balance()
        self.lblBalance.setText(f"Kasa Bakiyesi: {balance:.2f} TL")
