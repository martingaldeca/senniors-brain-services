import pandas as pd

from brain_services.transformers import BaseTransformer


class DataFrameColumnNamesTransformer(BaseTransformer):
    """
    This transformer will update the names of some columns of the dataframe in order to have a better naming for work
    with them
    """
    names_to_update_list: list = []

    def __init__(
        self,
        names_to_update_list: list = None
    ):
        """

        :param names_to_update_list: This is a list of tuples, with the following format:
            [
                (new_column_name_0, old_column_name_0),
                (new_column_name_1, old_column_name_1),
                ...
            ]
        """
        if names_to_update_list:
            self.names_to_update_list = names_to_update_list

    def transform(
        self,
        x: pd.DataFrame,
        y: pd.DataFrame = None
    ):
        columns_to_drop = []
        for name_to_update in self.names_to_update_list:
            final_name, original_name = name_to_update
            if original_name in x.columns:
                x[final_name] = x[original_name]
                columns_to_drop.append(original_name)

        if columns_to_drop:
            x = x.drop(columns=columns_to_drop)
        return x
