import pandas as pd

from brain_services.transformers import BaseTransformer


class ExtractDateTimeInfoTransformer(BaseTransformer):
    """
    This transformer extract data from a datetime column and set into another the property you want to extract, for
    example the day of the week, the month, the date...
    """
    base_column_name: str = None
    final_column_name: str = None
    info_to_extract: str = None

    def __init__(
        self,
        base_column_name: str,
        final_column_name: str,
        info_to_extract: str,
    ):
        """

        :param base_column_name: Column name where the datetime field is
        :param final_column_name: Column name where the data will be stored
        :param info_to_extract: Info to extract, it will be a property of datetime
        """
        self.base_column_name = base_column_name
        self.final_column_name = final_column_name
        self.info_to_extract = info_to_extract

    def transform(self, x: pd.DataFrame, y: pd.DataFrame = None):
        x[self.final_column_name] = getattr(x[self.base_column_name].dt, self.info_to_extract)
        return x
