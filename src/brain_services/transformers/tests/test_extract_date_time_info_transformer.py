from datetime import datetime
from unittest import TestCase

from brain_services.transformers import ExtractDateTimeInfoTransformer
from brain_services.transformers.tests import TesBaseTransformerMixin


class ExtractDateTimeInfoTransformerTest(TesBaseTransformerMixin, TestCase):
    transformer = ExtractDateTimeInfoTransformer
    input_data_frame_dict = {
        'row1': [
            datetime.strptime('1994-08-08T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        ]
    }
    output_data_frame_dict = {
        'row1': [
            datetime.strptime('1994-08-08T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            8
        ]
    }
    init_kwargs = {
        'base_column_name': 'column1',
        'final_column_name': 'test1',
        'info_to_extract': 'day'
    }
    initial_column_names = ['column1', ]
    final_column_names = ['column1', 'test1']
