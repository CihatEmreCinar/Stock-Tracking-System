def calculate_vat(amount, vat_rate):
    """KDV tutarını hesapla"""
    return amount * vat_rate / 100

def format_currency(amount):
    """Para birimini formatla"""
    return f"{amount:.2f} TL"
