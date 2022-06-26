from datetime import datetime
from unittest import TestCase

from brain_services.transformers import ExtractDaysBetweenDatesTransformer
from brain_services.transformers.tests import TesBaseTransformerMixin


class ExtractDaysBetweenDatesTransformerTest(TesBaseTransformerMixin, TestCase):
    transformer = ExtractDaysBetweenDatesTransformer
    input_data_frame_dict = {
        'row1': [
            datetime.strptime('1994-08-08T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            datetime.strptime('1994-07-28T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        ]
    }
    output_data_frame_dict = {
        'row1': [
            datetime.strptime('1994-08-08T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            datetime.strptime('1994-07-28T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            11
        ]
    }
    init_kwargs = {
        'final_column_name': 'test1',
        'greater_date_column_name': 'column1',
        'lower_date_column_name': 'column2'
    }
    initial_column_names = ['column1', 'column2']
    final_column_names = ['column1', 'column2', 'test1']
