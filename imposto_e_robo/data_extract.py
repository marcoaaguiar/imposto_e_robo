import imposto_e_robo.safeprint

import re

import fitz

doc = fitz.Document("input/267727_NotaCorretagem.pdf")

for page in doc:
    #  print(page.get_text())
    pattern = re.compile(
        r"""(?P<stockex>(?:\w|-)+)
(?P<buy_or_sell>C|V)
(?P<market>\w+)
(?P<stock>.+)
(?P<obs>\w?)
(?P<amount>(?:\d{0,3}\.)*\d{0,3})
(?P<price>(?:\d{0,3}\.)*\d{0,3},\d{2})
(?P<total>(?:\d{0,3}\.)*\d{0,3},\d{2})
(?P<credit_or_debit>D|C)""",
        flags=re.MULTILINE,
    )

    matches = pattern.findall(page.get_text())
    print(matches)
