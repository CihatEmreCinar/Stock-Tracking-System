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
    weight: float | None = None 

@dataclass
class Sale:
    id: int
    product_id: int
    quantity: int
    total_price: float
    date: str
    vat_amount: float | None = None

@dataclass
class CashRecord:
    id: int
    type: str
    amount: float
    date: str
