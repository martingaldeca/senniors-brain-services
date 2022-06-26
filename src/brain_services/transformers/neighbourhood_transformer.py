import pandas as pd
from unidecode import unidecode

from brain_services.transformers import BaseTransformer


class NeighbourhoodTransformer(BaseTransformer):
    """
    This transformer transform the neighbourhood field in a matrix that we can use to predict with numbers instead of
    strings.

    For example, if our column neighbourhood is
    """
    neighbourhood_column_name = 'neighbourhood'
    prefix = 'neighbourhood'

    def __init__(
        self,
        neighbourhood_column_name: str = None,
        prefix: str = None
    ):
        if neighbourhood_column_name:
            self.neighbourhood_column_name = neighbourhood_column_name
        if prefix:
            self.prefix = prefix

    def transform(self, x: pd.DataFrame, y: pd.DataFrame = None):
        # Check that the transformer can be used
        if self.neighbourhood_column_name not in x.keys():
            raise ValueError(f'Key {self.neighbourhood_column_name} must be in dataframe')

        # Transform data to optimize the dummies method
        x[self.neighbourhood_column_name] = x[self.neighbourhood_column_name].str.lower()
        x[self.neighbourhood_column_name] = x[self.neighbourhood_column_name].replace(' ', '_', regex=True)
        x[self.neighbourhood_column_name] = x[self.neighbourhood_column_name].apply(unidecode)  # Minor optimization

        neighbourhood_df = pd.get_dummies(x[self.neighbourhood_column_name], prefix=self.prefix)
        x = pd.concat([x, neighbourhood_df], axis=1)
        return x
