from dataclasses import dataclass

@dataclass
class Product:
    id: int
    barcode: str
    name: str
    cost_price: float
    sale_price: float
    vat_rate: float
    stock_quantity: int

@dataclass
class Sale:
    id: int
    product_id: int
    quantity: int
    total_price: float
    date: str

@dataclass
class CashRecord:
    id: int
    type: str
    amount: float
    date: str
