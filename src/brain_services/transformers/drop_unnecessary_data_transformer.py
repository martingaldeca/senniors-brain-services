import pandas as pd

from brain_services.transformers import BaseTransformer


class DropUnnecessaryDataTransformer(BaseTransformer):
    """
    This transformer will remove all unnecessary columns that we don't want to use in our trainings
    """
    unnecessary_columns: list = None

    def __init__(
        self,
        unnecessary_columns: list = None
    ):
        """

        :param unnecessary_columns: List or list of columns you want to drop from the dataframe, by default it is None
        """
        self.unnecessary_columns = unnecessary_columns

    def transform(
        self,
        x: pd.DataFrame,
        y: pd.DataFrame = None
    ):
        for unnecessary_column in self.unnecessary_columns:
            if unnecessary_column in x.columns:
                x = x.drop(columns=[unnecessary_column, ])
        return x
