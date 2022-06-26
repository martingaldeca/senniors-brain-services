import pandas as pd

from brain_services.transformers import BaseTransformer


class SwapInvalidDatesTransformer(BaseTransformer):
    """
    This transformer swap dates that are swapped
    """
    greater_date_column_name: str = None
    lower_date_column_name: str = None

    def __init__(
        self,
        greater_date_column_name: str,
        lower_date_column_name: str,
    ):
        """

        :param greater_date_column_name: Name of the column that should be higher
        :param lower_date_column_name: Name of the column that should be lowered
        """
        self.greater_date_column_name = greater_date_column_name
        self.lower_date_column_name = lower_date_column_name

    def transform(self, x: pd.DataFrame, y: pd.DataFrame = None):
        x_copy = x.copy()
        x_copy.loc[
            x[self.greater_date_column_name] < x[self.lower_date_column_name],
            self.greater_date_column_name
        ] = x[
            x[self.greater_date_column_name] < x[self.lower_date_column_name]
            ][self.lower_date_column_name]

        x_copy.loc[
            x[self.greater_date_column_name] < x[self.lower_date_column_name],
            self.lower_date_column_name
        ] = x[
            x[self.greater_date_column_name] < x[self.lower_date_column_name]
            ][self.greater_date_column_name]

        return x_copy
