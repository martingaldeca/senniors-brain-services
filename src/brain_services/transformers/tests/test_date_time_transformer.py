from datetime import datetime
from unittest import TestCase

from brain_services.transformers import DateTimeTransformer
from brain_services.transformers.tests import TesBaseTransformerMixin


class DateTimeTransformerTest(TesBaseTransformerMixin, TestCase):
    transformer = DateTimeTransformer
    input_data_frame_dict = {
        'row1': [
            '1994-08-08T00:00:00Z',
            '1994-07-28T00:00:00Z'
        ],
    }
    output_data_frame_dict = {
        'row1': [
            datetime.strptime('1994-08-08T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            '1994-07-28T00:00:00Z',
        ],
    }
    init_kwargs = {
        'column_name': 'column1',
        'format_to_use': '%Y-%m-%dT%H:%M:%SZ'
    }
    initial_column_names = ['column1', 'column2']
