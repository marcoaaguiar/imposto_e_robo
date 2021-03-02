import imposto_e_robo.safeprint
from pathlib import Path
from imposto_e_robo.data_extract import transactions_from_file


for file_path in Path("input/").glob("*.pdf"):
    print(transactions_from_file(file_path))
