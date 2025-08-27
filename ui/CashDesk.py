from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import services.cash_service as cash_service

class CashDeskPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Başlık
        self.lblTitle = QLabel("💰 Kasa Durumu")
        self.lblTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.lblTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lblTitle)

        # Bakiye etiketi
        self.lblBalance = QLabel()
        self.lblBalance.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.lblBalance.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lblBalance)

        # Yenile butonu
        btnLayout = QHBoxLayout()
        self.btnRefresh = QPushButton("🔄 Yenile")
        self.btnRefresh.clicked.connect(self.refresh_balance)
        btnLayout.addStretch()
        btnLayout.addWidget(self.btnRefresh)
        btnLayout.addStretch()
        layout.addLayout(btnLayout)

        self.setLayout(layout)
        self.refresh_balance()

    def refresh_balance(self):
        try:
            balance = cash_service.get_balance()
            self.lblBalance.setText(f"{balance:.2f} TL")

            # Bakiye pozitif/negatif renk kontrolü
            if balance >= 0:
                self.lblBalance.setStyleSheet("color: green;")
            else:
                self.lblBalance.setStyleSheet("color: red;")

        except Exception as e:
            self.lblBalance.setText("Kasa bakiyesi alınamadı!")
            self.lblBalance.setStyleSheet("color: gray;")
            QMessageBox.critical(self, "Hata", f"Kasa bilgisi alınırken bir hata oluştu: {e}")
