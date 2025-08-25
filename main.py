import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
from database.db import init_db
from ui.Stock import StockPage
from ui.Sells import SellsPage
from ui.CashDesk import CashDeskPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stok Takip Uygulaması")
        self.setGeometry(200, 100, 1000, 600)

        main_layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Sol Menü
        menu_layout = QVBoxLayout()
        btn_stock = QPushButton("📦 Stoklar")
        btn_sells = QPushButton("🛒 Satış")
        btn_cash = QPushButton("💰 Kasa")

        menu_layout.addWidget(btn_stock)
        menu_layout.addWidget(btn_sells)
        menu_layout.addWidget(btn_cash)
        menu_layout.addStretch()

        # Sağ Sayfalar
        self.pages = QStackedWidget()
        self.page_stock = StockPage()
        self.page_sells = SellsPage()
        self.page_cash = CashDeskPage()

        self.pages.addWidget(self.page_stock)
        self.pages.addWidget(self.page_sells)
        self.pages.addWidget(self.page_cash)

        btn_stock.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_stock))
        btn_sells.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_sells))
        btn_cash.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_cash))

        main_layout.addLayout(menu_layout, 1)
        main_layout.addWidget(self.pages, 4)

if __name__ == "__main__":
    init_db()  # Veritabanı başlat
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
 