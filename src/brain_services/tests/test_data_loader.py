from logging import getLogger
from unittest import mock, TestCase

import pandas as pd
from imblearn.under_sampling import RandomUnderSampler

from brain_services.data_loader import DataLoader


class DataLoaderTest(TestCase):

    def setUp(self) -> None:
        self.data_path = './brain_services/tests/test.csv'
        self.test_size = 0.2
        self.balanced_data = False
        self.y_column_name = 'No-show'
        self.random_state = 1

        self.valid_data_frame = pd.read_csv(self.data_path)

    def test_not_valid_data_path(self):
        data_path = 'not_valid_path.csv'
        with self.assertRaises(
            FileNotFoundError
        ), mock.patch.object(
            getLogger('brain_services.data_loader'), 'error'
        ) as mock_logger:
            DataLoader(
                data_path=data_path,
                test_size=self.test_size,
                balanced_data=self.balanced_data,
                y_column_name=self.y_column_name,
                random_state=self.random_state,
            )
        self.assertEqual(mock_logger.call_count, 1)
        self.assertEqual(
            mock_logger.call_args,
            mock.call(
                'Not valid data path',
                extra={
                    'data_path': data_path
                }
            )
        )

    def test_not_valid_csv(self):
        self.data_path = './main.py'
        with self.assertRaises(
            pd.errors.ParserError
        ), mock.patch.object(
            getLogger('brain_services.data_loader'), 'error'
        ) as mock_logger:
            DataLoader(
                data_path=self.data_path,
                test_size=self.test_size,
                balanced_data=self.balanced_data,
                y_column_name=self.y_column_name,
                random_state=self.random_state,
            )
        self.assertEqual(mock_logger.call_count, 1)
        self.assertEqual(
            mock_logger.call_args,
            mock.call(
                'Not valid format for file, it must be a csv',
                extra={
                    'data_path': self.data_path
                }
            )
        )

    def test_validate_parameters(self):
        test_data_list = [
            (-1, True, 'No-show', 'Test size not valid, must be between 0 and 1, not "-1"'),
            (0.5, 'not_valid', 'No-show', 'Balanced data not valid, must be True or False, not "not_valid"'),
            (0.5, True, 'not-valid', 'Y column name "not-valid" is not a valid column name'),
        ]
        for test_data in test_data_list:
            with self.subTest(
                test_data=test_data
            ), self.assertRaises(
                ValueError
            ) as expected_error:
                test_size, balanced_data, y_column_name, expected_message = test_data
                DataLoader(
                    data_path=self.data_path,
                    test_size=test_size,
                    balanced_data=balanced_data,
                    y_column_name=y_column_name,
                    random_state=self.random_state,
                )
            self.assertEqual(str(expected_error.exception), expected_message)

    def test_balanced_data(self):
        test_data_list = [
            (True, 1, 1, 1),
            (False, 0, 0, 0),
        ]
        for test_data in test_data_list:
            with mock.patch.object(
                RandomUnderSampler, '__init__'
            ) as mock_random_under_sampler_init, mock.patch.object(
                RandomUnderSampler, 'fit_resample'
            ) as mock_random_under_sampler_fit_resample, mock.patch.object(
                pd.DataFrame, 'assign'
            ) as mock_assign, self.subTest(
                test_data=test_data
            ), mock.patch.object(
                DataLoader, '_train_test_split'
            ):
                mock_random_under_sampler_init.return_value = None
                mock_random_under_sampler_fit_resample.return_value = pd.DataFrame(), pd.DataFrame()
                (
                    balanced_data,
                    mock_random_under_sampler_init_call_count,
                    mock_random_under_sampler_fit_resample_call_count,
                    mock_assign_call_count
                ) = test_data

                DataLoader(
                    data_path=self.data_path,
                    test_size=self.test_size,
                    balanced_data=balanced_data,
                    y_column_name=self.y_column_name,
                    random_state=self.random_state,
                )

                self.assertEqual(
                    mock_random_under_sampler_init.call_count,
                    mock_random_under_sampler_init_call_count
                )
                self.assertEqual(
                    mock_random_under_sampler_fit_resample.call_count,
                    mock_random_under_sampler_fit_resample_call_count
                )
                self.assertEqual(
                    mock_assign.call_count,
                    mock_assign_call_count
                )

    def test_train_test_split(self):
        with mock.patch(
            'brain_services.data_loader.train_test_split'
        ) as mock_train_test_split:
            mock_train_test_split.return_value = self.valid_data_frame, self.valid_data_frame
            data_loader = DataLoader(
                data_path=self.data_path,
                test_size=self.test_size,
                balanced_data=self.balanced_data,
                y_column_name=self.y_column_name,
                random_state=self.random_state,
            )
            self.assertEqual(mock_train_test_split.call_count, 1)
            self.assertEqual(
                mock_train_test_split.call_args,
                mock.call(
                    data_loader.df_to_use,
                    test_size=self.test_size,
                    random_state=self.random_state
                )
            )
