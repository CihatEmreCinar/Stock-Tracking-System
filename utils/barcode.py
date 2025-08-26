from PyQt6.QtCore import QObject, QEvent

class BarcodeScannerHID(QObject):
    def __init__(self, target_lineedit, on_scanned=None, min_length=3, clear_on_scan=True):
        super().__init__()
        self.target = target_lineedit
        self.buffer = ""
        self.on_scanned = on_scanned  # callback
        self.min_length = min_length
        self.clear_on_scan = clear_on_scan
        self.target.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.target and event.type() == QEvent.Type.KeyPress:
            key = event.text()
            if key == "\r":  # Enter tuşu → barkod tamamlandı
                barcode = self.buffer.strip()
                if len(barcode) >= self.min_length:
                    if self.clear_on_scan:
                        self.target.setText("")
                    else:
                        self.target.setText(barcode)
                    if self.on_scanned:
                        self.on_scanned(barcode)  # callback çağır
                self.buffer = ""
                return True
            else:
                self.buffer += key
        return super().eventFilter(obj, event)

    def set_callback(self, callback):
        """Dışarıdan callback atamak için"""
        self.on_scanned = callback
