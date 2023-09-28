import pandas as pd
from ingest_data.ingest_hijk_data import ingestCSVhijk
from ingest_data.io_operations import read_excel_data, write_to_json


if __name__ == "__main__":
    # Read Excel Data
    excel_data = pd.read_excel(
        "reliability/data/HIJK_sluitingen_bewerkt.xlsx")

    # Prepare and Process Data
    hijk_obj = ingestCSVhijk(excel_data)
    hijk_obj.prepare_dataframe()
    closure_data = hijk_obj.create_hijk_dict()

    # Write to JSON
    write_to_json(closure_data, "reliability/data/HIJK_closure_data.json")
