import csv
import dataclasses


def export_dataclass_to_csv(filename, items, cls=None, headers=None):
    if cls is not None:
        headers = [field.name for field in dataclasses.fields(cls)]
    if headers is None:
        raise ValueError(f"Neither cls or headers not defined")
    with open(filename, "w") as csv_file:
        dict_writer = csv.DictWriter(csv_file, headers)
        dict_writer.writeheader()

        for item in items:
            dict_writer.writerow(dataclasses.asdict(item))
