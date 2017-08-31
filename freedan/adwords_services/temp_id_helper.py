import pandas as pd


class TempIdHelper:
    def __init__(self):
        self._temp_id = 0

    @property
    def temp_id(self):
        self._temp_id -= 1
        return self._temp_id

    def fillna_with_temp_id(self, input_value):
        """ If id is np.nan, return new temporary id (negative int), else return the id"""
        if pd.isnull(input_value):
            return int(self.temp_id)
        return input_value
