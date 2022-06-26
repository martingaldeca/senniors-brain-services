from unittest import TestCase

from brain_services.transformers import DataFrameColumnNamesTransformer
from brain_services.transformers.tests import TesBaseTransformerMixin


class DataFrameColumnNamesTransformerTest(TesBaseTransformerMixin, TestCase):
    transformer = DataFrameColumnNamesTransformer
    input_data_frame_dict = {
        'row1': [1, 2, 3],
        'row2': [1, 2, 3],
    }
    output_data_frame_dict = {
        'row1': [3, 1, 2],
        'row2': [3, 1, 2],
    }
    init_kwargs = {
        'names_to_update_list': [
            ('test1', 'column1'),
            ('test2', 'column2')
        ]
    }
    initial_column_names = ['column1', 'column2', 'column3']
    final_column_names = ['column3', 'test1', 'test2']
