from logging import getLogger
from unittest import mock, TestCase

from brain_services.predictor import SenniorsPredictor


class SenniorsPredictorTest(TestCase):

    def test_trained_pipe_file_path_does_not_exists(self):

        with self.assertRaises(ValueError) as expected_exception:
            SenniorsPredictor(trained_pipe_file_path='not_valid.pkl')
        self.assertEqual(
            str(expected_exception.exception),
            '"not_valid.pkl" is not a valid trained pipe file'
        )

    def test_predict_problem_with_prediction(self):
        with mock.patch(
            'joblib.load'
        ) as mock_load_pipe, mock.patch.object(
            getLogger('brain_services.predictor'), 'error'
        ) as mock_logger, self.assertRaises(Exception):
            mock_pipe = mock.MagicMock()
            mock_pipe.predict.side_effect = Exception()
            mock_load_pipe.return_value = mock_pipe
            predictor = SenniorsPredictor(trained_pipe_file_path='main.py')
            predictor.predict(x='test')
        self.assertEqual(mock_logger.call_count, 1)
        self.assertEqual(
            mock_logger.call_args,
            mock.call(
                'There was a problem with the prediction',
                extra={
                    'x': 'test',
                }
            )
        )

    def test_predict_valid_prediction(self):

        test_data_list = [
            (['No', ], True),
            (['Yes', ], False),
        ]
        for test_data in test_data_list:
            with self.subTest(
                test_data=test_data
            ), mock.patch(
                'joblib.load'
            ) as mock_load_pipe, mock.patch.object(
                getLogger('brain_services.predictor'), 'error'
            ) as mock_error_logger, mock.patch.object(
                getLogger('brain_services.predictor'), 'debug'
            ) as mock_debug_logger:
                prediction, expected_result = test_data
                mock_pipe = mock.MagicMock()
                mock_pipe.predict.return_value = prediction
                mock_load_pipe.return_value = mock_pipe
                predictor = SenniorsPredictor(trained_pipe_file_path='main.py')
                self.assertEqual(predictor.predict(x='test'), expected_result)
                self.assertEqual(mock_error_logger.call_count, 0)
                self.assertEqual(mock_debug_logger.call_count, 1)
                self.assertEqual(
                    mock_debug_logger.call_args,
                    mock.call(
                        f'The prediction was "{prediction}", input data was "test"'
                    )
                )
