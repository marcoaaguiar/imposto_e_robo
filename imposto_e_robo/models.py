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


@dataclass
class BrokerageReceipt:
    net_operation_value: Decimal
    liquidation_fee: Decimal
    registration_fee: Decimal

    options_fee: Decimal
    ana_total: Decimal
    emoluments: Decimal

    operational_fee: Decimal
    execution: Decimal
    custody_fee: Decimal
    taxes: Decimal
    irrf_wo_operation: Decimal
    others: Decimal

    @property
    def total_cblc(self) -> Decimal:
        return self.net_operation_value + self.liquidation_fee + self.registration_fee

    @property
    def total_bovespa(self) -> Decimal:
        return self.options_fee + self.ana_total + self.emoluments

    @property
    def total_costs(self) -> Decimal:
        return (
            self.operational_fee
            + self.execution
            + self.custody_fee
            + self.taxes
            + self.irrf_wo_operation
            + self.others
        )

    @property
    def net_value_for_date(self) -> Decimal:
        return self.total_cblc + self.total_bovespa + self.total_costs

    @property
    def total(self) -> Decimal:
        return self.net_value_for_date
