import csv
import json
from typing import List, Dict


def load_data_in_memory() -> List[Dict]:
    """
    Load the file used as DB in memory.
    :return: List of dictionaries. Each dictionary represents one row in the CSV file.
    """
    with open("app/company.csv", "r") as company_file:
        reader = csv.DictReader(company_file)
        file_data = [json.loads(json.dumps(row)) for i, row in enumerate(reader)]

    return file_data
