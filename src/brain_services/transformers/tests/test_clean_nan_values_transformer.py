from unittest import TestCase

from brain_services.transformers import CleanNanValuesTransformer
from brain_services.transformers.tests import TesBaseTransformerMixin


class CleanNanValuesTransformerTest(TesBaseTransformerMixin, TestCase):
    transformer = CleanNanValuesTransformer
    input_data_frame_dict = {
        'row1': [1, None, 3],
        'row2': [1, 2, 3],
    }
    output_data_frame_dict = {
        'row2': [1, 2.0, 3],
    }
    init_kwargs = {
        'strategy': 'dropna',
        'strategy_kwargs': {
            'inplace': True
        }
    }
    column_names = ['column1', 'column2', 'column3']
