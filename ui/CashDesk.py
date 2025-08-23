from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
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
        try:
            balance = cash_service.get_balance()
            self.lblBalance.setText(f"Kasa Bakiyesi: {balance:.2f} TL")
            QMessageBox.information(self, "Kasa Durumu", f"Güncel kasa bakiyesi: {balance:.2f} TL")
        except Exception as e:
            # Kasa bilgisi alınamazsa hata mesajı göster
            self.lblBalance.setText("Kasa bakiyesi alınamadı!")
            QMessageBox.critical(self, "Hata", f"Kasa bilgisi alınırken bir hata oluştu: {e}")
