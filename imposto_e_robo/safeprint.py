import builtins
import os
import re
from typing import Any

old_print = builtins.print


def multireplace(
    paragraph: str, replacements: dict[str, str], ignore_case: bool = False
) -> str:
    """
    Given a string and a replacement map, it returns the replaced string.
    :param string: string to execute replacements on
    :param replacements: replacement dictionary {value to find: value to replace}
    :param ignore_case: whether the match should be case insensitive
    """

    replacements = {key.lower(): val for key, val in replacements.items()}

    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    # 'hey ABC' and not 'hey ABc'
    rep_sorted = sorted(replacements, key=len, reverse=True)
    rep_escaped = [re.escape(rep) for rep in rep_sorted]

    # Create a big OR regex that matches any of the substrings to replace
    pattern = re.compile("|".join(rep_escaped), re.IGNORECASE)

    # For each match, look up the new string in the replacements, being the key the normalized old string
    return pattern.sub(lambda match: replacements[match.group(0).lower()], paragraph)


def new_print(*args: str, **kwargs: Any):
    replacements = {
        os.environ["CPF"]: "123.456.678-90",
        os.environ["PHONE"]: "(099) 1234-6789",
        os.environ["NAME"]: "MARCO AGUIAR",
        os.environ["ADDRESS"]: "R DA PATOTA 69, 420 - TERRA DOS",
        os.environ["ADDRESS2"]: "COQUEIROS",
        os.environ["ZIPCODE"]: "12345-123",
        os.environ["BANK_ACCOUNT"]: "1324353",
    }

    args = tuple(multireplace(str(arg), replacements) for arg in args)

    old_print(*args, **kwargs)


builtins.print = new_print
