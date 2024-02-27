import csv
import numpy as np
from io import StringIO
from .methods.MCDMFactory import MCDAMethodFactory


class CSVDataProcessor:
    mcdm_factory = MCDAMethodFactory()

    def __init__(self, method_name, binary_csv_data):
        self.method_name = method_name

        types, weights, decision_matrix, bounds = self._parse_data(binary_csv_data)
        self.method = self.mcdm_factory(method_name)
        method_args = [decision_matrix, weights, types]

        if method_name == "spotis":
            method_args.append(bounds)

        self.method(*method_args)
        self._preferences = self.method.get_preferences()
        self._ranking = self.method.get_ranking()
        self._alts_number = decision_matrix.shape[0]

    def _parse_data(self, binary_csv_data):
        data = binary_csv_data.decode("utf-8")
        if not data:
            raise ValueError("Empty CSV data")
        
        csv_reader = csv.reader(StringIO(data))
        types = self.validate_and_convert_to_ndarray(next(csv_reader), dtype=int)
        weights = self.validate_and_convert_to_ndarray(next(csv_reader), dtype=float)

        if self.method_name == "spotis":
            bounds = self.validate_and_convert_to_ndarray(next(csv_reader), dtype=float)
            bounds = bounds.reshape((bounds.shape[0] // 2, 2))

        else:
            bounds = None

        decision_matrix = np.array(list(csv_reader), dtype=float)

        return types, weights, decision_matrix, bounds

    def validate_and_convert_to_ndarray(self, row, dtype):
        try:
            return np.array(row, dtype=dtype)
        except ValueError as e:
            raise ValueError(f"Invalid data")
        

    @property
    def preferences(self):
        return self._preferences

    @property
    def ranking(self):
        return self._ranking

    @property
    def alts_number(self):
        return self._alts_number
