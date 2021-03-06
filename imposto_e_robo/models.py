from dataclasses import dataclass, field
from decimal import Decimal
import decimal
from typing import Optional


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

    @property
    def parsed_amount(self) -> int:
        if self.buy_or_sell == "C":
            return self.amount
        return -self.amount

    @property
    def is_daytrade(self) -> bool:
        return "d" in self.obs.lower()


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

    # TODO: pegar data

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


@dataclass
class Realization:
    stock: str
    amount: int
    entry_average_price: Decimal
    close_price: Decimal
    is_buy: bool
    #  date: datetime

    @property
    def total(self) -> Decimal:
        return self.amount * self.entry_average_price

    @property
    def net_value(self):
        value = (self.close_price - self.entry_average_price) * self.amount

        if self.is_buy:
            return value
        return -value


@dataclass
class PortfolioEntry:
    stock: str
    amount: int = 0
    average_price: Decimal = Decimal(0)

    def process_transaction(self, transaction: Transaction) -> Optional[Realization]:
        if self.stock != transaction.stock:
            raise ValueError(
                f"Transaction.stock and PortfolioEntry.stock are not the same: {self.stock}!={transaction.stock}"
            )

        if transaction.buy_or_sell == "C":
            try:
                self.average_price = (
                    self.average_price * self.amount
                    + transaction.price * transaction.amount
                ) / (self.amount + transaction.parsed_amount)
            except decimal.DivisionByZero:
                __import__("ipdb").set_trace()

            self.amount += transaction.parsed_amount
            return None

        # if some stock was sold
        realization_amount = min(self.amount, transaction.amount)
        self.amount += transaction.parsed_amount
        return Realization(
            stock=self.stock,
            amount=realization_amount,
            entry_average_price=self.average_price,
            close_price=transaction.price,
            is_buy=True,
        )
