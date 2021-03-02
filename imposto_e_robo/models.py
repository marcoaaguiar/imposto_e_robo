from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Transaction:
    stock_exchange: str
    buy_or_sell: str
    market: str
    obs: str
    stock: str
    amount: int
    price: Decimal
    credit_or_debit: str

    @property
    def total(self) -> Decimal:
        return self.amount * self.price
