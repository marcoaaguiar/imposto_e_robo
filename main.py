import imposto_e_robo.safeprint
from pathlib import Path
from imposto_e_robo.data_extract import (
    brokerage_receipt_from_file,
    transactions_from_file,
)
import fitz


for file_path in Path("input/").glob("*4.pdf"):
    doc = fitz.Document(str(file_path))
    print("receipt", brokerage_receipt_from_file(doc))
    print("transactions", transactions_from_file(doc))
