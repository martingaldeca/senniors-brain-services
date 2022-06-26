from unittest import TestCase

from brain_services.transformers import SwapInvalidDatesTransformer
from brain_services.transformers.tests import TesBaseTransformerMixin


class SwapInvalidDatesTransformerTest(TesBaseTransformerMixin, TestCase):
    transformer = SwapInvalidDatesTransformer
    input_data_frame_dict = {
        'row1': [
            3,
            1,
        ]
    }
    output_data_frame_dict = {
        'row1': [
            1,
            3
        ]
    }
    init_kwargs = {
        'greater_date_column_name': 'column2',
        'lower_date_column_name': 'column1'
    }
    initial_column_names = ['column1', 'column2']
    final_column_names = ['column1', 'column2']
