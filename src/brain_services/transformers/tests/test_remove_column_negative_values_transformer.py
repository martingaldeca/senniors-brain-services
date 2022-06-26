from unittest import TestCase

from brain_services.transformers import RemoveColumnNegativeValuesTransformer
from brain_services.transformers.tests import TesBaseTransformerMixin


class RemoveColumnNegativeValuesTransformerTest(TesBaseTransformerMixin, TestCase):
    transformer = RemoveColumnNegativeValuesTransformer
    input_data_frame_dict = {
        'row1': [
            -1,
            3,
        ]
    }
    output_data_frame_dict = {
        'row1': [
            0,
            3
        ]
    }
    init_kwargs = {
        'column_name': 'column1',
    }
    initial_column_names = ['column1', 'column2']
    final_column_names = ['column1', 'column2']
