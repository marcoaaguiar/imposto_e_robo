from datetime import date, datetime
from decimal import Decimal
import inspect
import re
from typing import List, Match

import fitz

from imposto_e_robo.models import BrokerageReceipt, Transaction
from imposto_e_robo.regex_strings import (
    RICO_BROKERAGE_RECEIPT_PATTERN_STRING,
    RICO_PATTERN_STRING,
)


RICO_TRANSACTION_PATTERN = re.compile(inspect.cleandoc(RICO_PATTERN_STRING))
RICO_BROKERAGE_RECEIPT_PATTERN = re.compile(
    inspect.cleandoc(RICO_BROKERAGE_RECEIPT_PATTERN_STRING), flags=re.MULTILINE
)


def get_date_from_file(doc: fitz.Document) -> date:
    """
    Data pregão
    26/10/2020
    """
    pattern = "Data pregão\n(\d\d/\d\d/\d\d\d\d)"
    for page in doc:
        match = re.search(pattern, page.get_text())
        if match:
            return datetime.strptime(match.group(1), "%d/%m/%Y").date()
    raise ValueError(f"Date not found in file {doc}")


def brokerage_receipt_from_file(doc: fitz.Document) -> BrokerageReceipt:
    for page in doc:
        match = RICO_BROKERAGE_RECEIPT_PATTERN.search(page.get_text())

        if match:
            return parse_brokerage_recipt_match(match)
    raise ValueError(f"No brokerage receipt found in file: {doc}")


def parse_brokerage_recipt_match(match: re.Match) -> BrokerageReceipt:
    match_dict = match.groupdict()

    total_cblc = Decimal(br_to_us_number_format(match_dict.pop("total_cblc")))
    total_bovespa = Decimal(br_to_us_number_format(match_dict.pop("total_bovespa")))
    total_costs = Decimal(br_to_us_number_format(match_dict.pop("total_costs")))
    net_value_for_date = Decimal(
        br_to_us_number_format(match_dict.pop("net_value_for_date"))
    )

    fields_as_decimal_dict = {
        field: Decimal(br_to_us_number_format(field_value))
        for field, field_value in match_dict.items()
    }

    receipt = BrokerageReceipt(**fields_as_decimal_dict)

    assert total_cblc == receipt.total_cblc
    assert total_bovespa == receipt.total_bovespa
    assert total_costs == receipt.total_costs
    assert net_value_for_date == receipt.net_value_for_date

    return receipt


def transactions_from_file(doc: fitz.Document) -> List[Transaction]:
    transactions = []
    for page in doc:
        for match in RICO_TRANSACTION_PATTERN.finditer(page.get_text()):
            transactions.append(parse_transaction_match(match))

    if len(transactions) == 0:
        raise ValueError("No transactions found in file")
    # verify emoluments
    return transactions


def parse_transaction_match(match: Match[str]) -> Transaction:
    match_dict = match.groupdict()

    total = Decimal(br_to_us_number_format(match_dict.pop("total")))

    match_dict["stock"] = re.sub(r"\s+", " ", match_dict["stock"])
    match_dict["amount"] = int(br_to_us_number_format(match_dict["amount"]))
    match_dict["price"] = Decimal(br_to_us_number_format(match_dict["price"]))

    # TODO: fix regex
    match_dict["obs"] = match_dict["obs"].strip()

    trans = Transaction(**match_dict)
    assert trans.total == total, "Total extraído não bate com o da nota"

    return trans


def br_to_us_number_format(numb_str: str) -> str:
    """
    Removes dot as thousand separator and replaces comma decimal separator with dot

    >>> br_to_us_number_format('10.000,00')
    '10000.00'
    """
    return numb_str.replace(".", "").replace(",", ".")
