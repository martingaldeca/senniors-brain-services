import pandas as pd

from brain_services.transformers import BaseTransformer


class DateTimeTransformer(BaseTransformer):
    """
    This transformer transform one str with some format to a datetime in order to work better with the data
    """
    format_to_use: str = None

    def __init__(
        self,
        column_name: str,
        format_to_use: str,
    ):
        """

        :param column_name: The column name to update to datetime
        :param format_to_use: The format to use for the transformer
        """
        self.column_name = column_name
        self.format_to_use = format_to_use

    def transform(self, x: pd.DataFrame, y: pd.DataFrame = None):
        x[self.column_name] = pd.to_datetime(x[self.column_name], format=self.format_to_use)
        return x
