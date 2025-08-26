# utils/barcode_scanner.py
# USB el terminali (HID klavye) için barkod adaptörü

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QTimer

class BarcodeScannerHID:
    """
    Bir QLineEdit'e bağlanır. Barkod okuyucu Enter gönderince callback'e kodu iletir.
    Kamera/pyzbar/seri-port gerekmez.
    """
    def __init__(self, line_edit: QLineEdit, on_scanned=None, *, min_length: int = 3, clear_on_scan: bool = False):
        self.line_edit = line_edit
        self.on_scanned = on_scanned
        self.min_length = min_length
        self.clear_on_scan = clear_on_scan

        # Çoğu barkod okuyucu Enter ile biter → returnPressed yeterli.
        self.line_edit.returnPressed.connect(self._emit_code)

        # İsteğe bağlı: Enter göndermeyen okuyucular için kısa bir zamanlayıcı ile "burst" yakalama.
        self._burst_timer = QTimer(self.line_edit)
        self._burst_timer.setSingleShot(True)
        self._burst_timer.timeout.connect(self._emit_code)
        self.line_edit.textEdited.connect(self._restart_burst_timer)

    def _restart_burst_timer(self, _text: str):
        # 80–120ms arası genelde güvenli. Okuyucu “Enter” göndermiyorsa devreye girer.
        self._burst_timer.start(120)

    def _emit_code(self):
        code = (self.line_edit.text() or "").strip()
        if len(code) >= self.min_length and self.on_scanned:
            try:
                self.on_scanned(code)
            finally:
                if self.clear_on_scan:
                    self.line_edit.clear()
