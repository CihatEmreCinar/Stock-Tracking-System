# barcode.py
import serial

class BarcodeScanner:
    def __init__(self, port="COM3", baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
        except Exception as e:
            print(f"Seri port açma hatası: {e}")
            self.ser = None

    def read_barcode(self):
        if not self.ser:
            raise Exception("Seri port bağlı değil")
        line = self.ser.readline().decode("utf-8").strip()
        return line
