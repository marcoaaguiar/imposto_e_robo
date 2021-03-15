import csv
import dataclasses


def export_dataclass_to_csv(filename, items, cls):
    headers = [field.name for field in dataclasses.fields(cls)]
    with open(filename, "w") as csv_file:
        dict_writer = csv.DictWriter(csv_file, headers)
        dict_writer.writeheader()

        for item in items:
            dict_writer.writerow(dataclasses.asdict(item))
