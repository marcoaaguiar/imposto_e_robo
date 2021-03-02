from decimal import Decimal
import inspect
import re
from typing import List, Match, Union
from pathlib import Path

import fitz

from imposto_e_robo.models import Transaction

RICO_PATTERN_STRING = r"""(?P<stock_exchange>(?:\w|-)+)
                    (?P<buy_or_sell>C|V)
                    (?P<market>\w+)
                    (?P<stock>.+)(?P<obs>(\n\w)?)
                    (?P<amount>(?:\d{0,3}\.)*\d{0,3})
                    (?P<price>(?:\d{0,3}\.)*\d{0,3},\d{2})
                    (?P<total>(?:\d{0,3}\.)*\d{0,3},\d{2})
                    (?P<credit_or_debit>D|C)"""

RICO_PATTERN = re.compile(inspect.cleandoc(RICO_PATTERN_STRING))


def transactions_from_file(file_path: Union[Path, str]) -> List[Transaction]:
    doc = fitz.Document(str(file_path))
    transactions = []
    for page in doc:
        for match in RICO_PATTERN.finditer(page.get_text()):
            transactions.append(parse_match(match))

    # verify emoluments
    return transactions


def parse_match(match: Match[str]) -> Transaction:
    match_dict = match.groupdict()

    total = Decimal(br_to_us_number_format(match_dict.pop("total")))

    match_dict["stock"] = re.sub(r"\s+", " ", match_dict["stock"])
    match_dict["amount"] = Decimal(br_to_us_number_format(match_dict["amount"]))
    match_dict["price"] = Decimal(br_to_us_number_format(match_dict["price"]))

    trans = Transaction(**match_dict)
    assert trans.total == total, "Total extraído não bate com o da nota"

    return trans


def br_to_us_number_format(numb_str: str) -> str:
    """
    Removes dot as thousand separator and replaces comma decimal separator with dot
    eg: 10.000,00 -> 10000.00
    """
    return numb_str.replace(".", "").replace(",", ".")
