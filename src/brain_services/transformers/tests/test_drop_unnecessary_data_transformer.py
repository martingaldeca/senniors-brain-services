from unittest import TestCase

from brain_services.transformers import DropUnnecessaryDataTransformer
from brain_services.transformers.tests import TesBaseTransformerMixin


class DropUnnecessaryDataTransformerTest(TesBaseTransformerMixin, TestCase):
    transformer = DropUnnecessaryDataTransformer
    input_data_frame_dict = {
        'row1': [1, 2, 3],
        'row2': [1, 2, 3],
    }
    output_data_frame_dict = {
        'row1': [2, 3],
        'row2': [2, 3],
    }
    init_kwargs = {
        'unnecessary_columns': ['column1', ]
    }
    initial_column_names = ['column1', 'column2', 'column3']
    final_column_names = ['column2', 'column3']
