import pandas as pd

from brain_services.transformers import BaseTransformer


class RemoveColumnNegativeValuesTransformer(BaseTransformer):
    """
    This transformer assumes that all the negative values can be changed by 0
    """

    def __init__(self, column_name: str):
        """

        :param column_name: The column to change all negative values to 0
        """
        self.column_name = column_name

    def transform(self, x: pd.DataFrame, y: pd.DataFrame = None):
        x.loc[x[self.column_name] < 0, self.column_name] = 0
        return x
