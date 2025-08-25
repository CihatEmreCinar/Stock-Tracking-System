class BarcodeScanner:
    def __init__(self, line_edit_widget):
        self.line_edit = line_edit_widget
        self.line_edit.returnPressed.connect(self._on_barcode_scanned)
        self._callback = None

    def set_callback(self, callback):
        self._callback = callback

    def _on_barcode_scanned(self):
        barcode = self.line_edit.text().strip()
        if not barcode:
            return
        if self._callback:
            self._callback(barcode)
        self.line_edit.clear()
