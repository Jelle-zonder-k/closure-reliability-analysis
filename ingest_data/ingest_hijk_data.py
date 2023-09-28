import numpy as np
import math
import pandas as pd
from datetime import datetime
from ingest_data.io_operations import read_excel_data, write_to_json


class ingestCSVhijk:
    def __init__(self, sheet: str):
        self.sheet = sheet
        self.barrier_abbreviation = "HIJK"  # Set the abbreviation directly
        self.closure_record = []

    def prepare_time_string(self):
        self.sheet.START = self.sheet['START'].replace(" ", "", regex=True)
        self.sheet.START = self.sheet['START'].replace("h", ":", regex=True)
        self.sheet.END = self.sheet['END'].replace(" ", "", regex=True)
        self.sheet.END = self.sheet['END'].replace("h", ":", regex=True)

    def handle_time_inputs(self, timestr):
        if timestr == '24:00':
            timestr = '00:00'
            time = datetime.strptime(timestr, '%H:%M').time()
            return str(time)
        elif ":" not in str(timestr):
            return None
        elif "oo" in str(timestr):
            corrected_time = str(timestr).replace('oo', '00')
            time = datetime.strptime(corrected_time, '%H:%M').time()
            return str(time)
        elif "." in str(timestr):
            corrected_time = str(timestr).replace('.', '')
            time = datetime.strptime(corrected_time, '%H:%M').time()
            return str(time)
        else:
            time = datetime.strptime(timestr, '%H:%M').time()
            return str(time)

    def prepare_date_string(self):
        self.sheet.DATE = self.sheet['DATE'].replace("`", "", regex=True)

    def prepare_waterlevel_string(self):
        self.sheet.WATERLEVEL = self.sheet['WATERLEVEL'].replace(
            " ", "", regex=True)
        self.sheet.WATERLEVEL = self.sheet['WATERLEVEL'].replace(
            ",", ".", regex=True)

    def set_type(self):
        TYPE = self.sheet['TYPE']

        # Assign values based on conditions
        self.sheet.loc[TYPE == 'stormsluiting', 'TYPE'] = 'STORM'
        self.sheet.loc[TYPE == 'testsluiting', 'TYPE'] = 'TEST'
        self.sheet.loc[(TYPE == 'functionelesluiting') | (
            TYPE == 'onderhoudsluiting'), 'TYPE'] = 'OPS'

    def check_if_row_is_record(self, record):
        return not math.isnan(record)

    def prepare_dataframe(self):
        self.prepare_time_string()
        self.prepare_date_string()
        self.prepare_waterlevel_string()
        self.set_type()
        return

    def create_hijk_dict(self):
        self.prepare_dataframe()
        df = self.sheet
        for index, row in df.iterrows():
            if not pd.isna(row.NUMBER):
                i = index
                while df.iloc[i].END == '--' or df.iloc[i].END == '':
                    i += 1
                self.closure_record.append({
                    'StartDate': str(pd.to_datetime(row.DATE).date()),
                    'StartTime': self.handle_time_inputs(row.START),
                    'EndDate': str(pd.to_datetime(df.iloc[i].DATE).date()),
                    'EndTime': self.handle_time_inputs(df.iloc[i].END),
                    'WaterLevel': row.WATERLEVEL,
                    'ClosureEventType': row.TYPE
                })
        return self.closure_record
