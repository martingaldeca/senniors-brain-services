import pandas as pd

from brain_services.transformers import BaseTransformer


class ExtractDaysBetweenDatesTransformer(BaseTransformer):
    """
    This transformer extract days between 2 dates of the dataframe
    """
    final_column_name: str = None
    greater_date_column_name: str = None
    lower_date_column_name: str = None

    def __init__(
        self,
        final_column_name: str,
        greater_date_column_name: str,
        lower_date_column_name: str,
    ):
        """

        :param final_column_name: The column name to store the extracted data
        :param greater_date_column_name: The column name of the greater date
        :param lower_date_column_name: The column name of the lower date
        """
        self.final_column_name = final_column_name
        self.greater_date_column_name = greater_date_column_name
        self.lower_date_column_name = lower_date_column_name

    def transform(self, x: pd.DataFrame, y: pd.DataFrame = None):
        x[self.final_column_name] = (x[self.greater_date_column_name] - x[self.lower_date_column_name]).dt.days
        return x
