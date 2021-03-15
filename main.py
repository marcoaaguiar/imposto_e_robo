from imposto_e_robo.csv_exporter import export_dataclass_to_csv
import imposto_e_robo.safeprint

from pathlib import Path
from typing import Dict, List

import fitz

from imposto_e_robo.data_extract import transactions_from_file
from imposto_e_robo.models import PortfolioEntry, Realization, Transaction

if __name__ == "__main__":
    transactions: List[Transaction] = []
    for file_path in Path("input/").glob("*.pdf"):
        doc = fitz.Document(str(file_path))
        #  print("receipt", brokerage_receipt_from_file(doc))
        transactions.extend(transactions_from_file(doc))

    portfolio: Dict[str, PortfolioEntry] = {}
    realizations: List[Realization] = []

    for transaction in transactions:
        if transaction.stock not in portfolio:
            portfolio[transaction.stock] = PortfolioEntry(stock=transaction.stock)

        realization = portfolio[transaction.stock].process_transaction(transaction)

        if realization is None:
            continue

        realizations.append(realization)

    export_dataclass_to_csv("transactions.csv", transactions, Transaction)
    export_dataclass_to_csv("realizations.csv", realizations, Realization)
