from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit, QFileDialog
from PyQt6.QtCore import QDate
import pandas as pd
import services.sales_service as sales_service

class SalesHistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Tarih seçiciler
        date_layout = QHBoxLayout()
        self.startDate = QDateEdit(QDate.currentDate().addMonths(-1))
        self.startDate.setCalendarPopup(True)
        self.endDate = QDateEdit(QDate.currentDate())
        self.endDate.setCalendarPopup(True)

        btnFilter = QPushButton("Filtrele")
        btnFilter.clicked.connect(self.refresh_table)
        btnExport = QPushButton("Excel’e Aktar")
        btnExport.clicked.connect(self.export_to_excel)

        date_layout.addWidget(self.startDate)
        date_layout.addWidget(self.endDate)
        date_layout.addWidget(btnFilter)
        date_layout.addWidget(btnExport)

        # Tablo
        self.table = QTableWidget()

        layout.addLayout(date_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        start = self.startDate.date().toPyDate()
        end = self.endDate.date().toPyDate()
        sales = sales_service.list_sales_by_date(start, end, limit=100)

        self.table.setRowCount(len(sales))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Ürün", "Adet", "Tutar", "Tarih"])

        for i, s in enumerate(sales):
            for j, val in enumerate(s):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def export_to_excel(self):
        start = self.startDate.date().toPyDate()
        end = self.endDate.date().toPyDate()
        sales = sales_service.list_sales_by_date(start, end, limit=10000)  # tümünü çek

        path, _ = QFileDialog.getSaveFileName(self, "Excel’e Kaydet", "", "Excel Files (*.xlsx)")
        if path:
            df = pd.DataFrame(sales, columns=["ID", "Ürün", "Adet", "Tutar", "Tarih"])
            df.to_excel(path, index=False)
