from decimal import Decimal
import imposto_e_robo.safeprint

from imposto_e_robo.csv_exporter import export_dataclass_to_csv

from datetime import date
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple
from collections import defaultdict

import fitz

from imposto_e_robo.data_extract import (
    brokerage_receipt_from_file,
    get_date_from_file,
    transactions_from_file,
)
from imposto_e_robo.models import PortfolioEntry, Realization, Transaction

YearMonth = NamedTuple("YearMonth", [("year", int), ("month", int)])


if __name__ == "__main__":
    transactions: List[Transaction] = []
    transactions_by_date: Dict[date, List[Transaction]] = {}
    receipts = []
    for file_path in Path("input/").glob("*.pdf"):
        doc = fitz.Document(str(file_path))
        brokerage_date = get_date_from_file(doc)
        brokerage_transactions = transactions_from_file(doc)

        transactions.extend(brokerage_transactions)
        transactions_by_date[brokerage_date] = transactions
        #  receipts.append(brokerage_receipt_from_file(doc))

    portfolio: Dict[str, PortfolioEntry] = {}
    realizations_by_month_year: Dict[YearMonth, List[Realization]] = defaultdict(list)

    transactions_by_date = dict(
        sorted(transactions_by_date.items(), key=lambda t: t[0])
    )
    for date, transaction_list in transactions_by_date.items():
        for transaction in transaction_list:
            if transaction.stock not in portfolio:
                portfolio[transaction.stock] = PortfolioEntry(stock=transaction.stock)

            realization = portfolio[transaction.stock].process_transaction(transaction)

            if realization is None:
                continue

            realizations_by_month_year[YearMonth(date.year, date.month)].append(
                realization
            )
    net_value_by_month_year = {
        month_year: sum(realization.net_value for realization in realizations)
        for month_year, realizations in realizations_by_month_year.items()
    }

    nontaxed_month_year = {
        month_year
        for month_year, realizations in realizations_by_month_year.items()
        if sum(realization.amount for realization in realizations) < 20_000
        and net_value_by_month_year[month_year] > 0
    }

    irf_table = [
        {
            "month_year": f"{month_year.year}/{month_year.month}",
            "net_value": net_value_by_month_year[month_year],
        }
        for month_year, realization in net_value_by_month_year.items()
    ]

    export_dataclass_to_csv(
        "irf_table.csv", irf_table, headers=["month_year", "net_value"]
    )
    #  __import__("pprint").pprint(transactions)
    #  __import__("pprint").pprint(realizations)
    #
    #  export_dataclass_to_csv("transactions.csv", transactions, Transaction)
    #  export_dataclass_to_csv("realizations.csv", realizations, Realization)
