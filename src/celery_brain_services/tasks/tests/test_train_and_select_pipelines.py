from logging import getLogger
from unittest import mock, TestCase

import numpy as np
from imblearn.pipeline import Pipeline

from brain_services.data_loader import DataLoader
from celery_brain_services.tasks.train_and_select_pipelines import train_and_select_pipelines
from settings import TRAINED_FILE_PATH


class TrainAndSelectPipelinesTest(TestCase):

    def test_train_call(self):
        mocked_names_to_update_list = []
        mocked_models_to_update_list = [
            ('test_model', mock.MagicMock()),
        ]
        mocked_base_steps = [('step_1', mock.MagicMock()), ('step_2', mock.MagicMock())]
        mocked_pca_optimization_components = [1, ]
        mock_pca = mock.MagicMock()

        with mock.patch(
            'celery_brain_services.tasks.train_and_select_pipelines.time.process_time',
            return_value=0.
        ), mock.patch.object(
            DataLoader,
            'data_path',
            new_callable=mock.PropertyMock
        ) as mock_data_path, mock.patch.object(
            DataLoader,
            'random_state',
            new_callable=mock.PropertyMock
        ) as mock_random_state, mock.patch.object(
            Pipeline, 'fit'
        ), mock.patch(
            'celery_brain_services.tasks.train_and_select_pipelines.cross_val_score'
        ) as mock_cross_val_score, mock.patch.object(
            getLogger('celery_brain_services.tasks.train_and_select_pipelines'), 'info'
        ) as mock_logger, mock.patch(
            'celery_brain_services.tasks.train_and_select_pipelines.joblib.dump'
        ) as mock_joblib_dump, mock.patch(
            'celery_brain_services.tasks.settings.NAMES_TO_UPDATE_LIST',
            mocked_names_to_update_list
        ), mock.patch(
            'celery_brain_services.tasks.train_and_select_pipelines.MODELS_TO_USE_LIST',
            mocked_models_to_update_list
        ), mock.patch(
            'celery_brain_services.tasks.train_and_select_pipelines.BASE_STEPS',
            mocked_base_steps
        ), mock.patch(
            'celery_brain_services.tasks.train_and_select_pipelines.PCA_OPTIMIZATION_COMPONENTS',
            mocked_pca_optimization_components
        ), mock.patch(
            'celery_brain_services.tasks.train_and_select_pipelines.PCA',
            mock_pca
        ):
            mock_data_path.return_value = './brain_services/tests/test.csv'
            mock_random_state.return_value = 1994
            mock_cross_val_score.return_value = np.array([1., 1., 1.])  # MAGIC!

            train_and_select_pipelines()
            self.assertEqual(mock_joblib_dump.call_count, 1)
            self.assertEqual(
                str(
                    mock_joblib_dump.call_args
                ),
                str(
                    mock.call(
                        Pipeline(
                            steps=(
                                mocked_base_steps +
                                [('pca_optimization_with_1_components', mock_pca(n_components=1)), ] +
                                [mocked_models_to_update_list[0], ]
                            )
                        ),
                        f'{TRAINED_FILE_PATH}best_pipe.pkl'
                    )
                )
            )
            self.assertEqual(mock_logger.call_count, 6)
            self.assertEqual(
                mock_logger.call_args_list,
                [
                    mock.call('Fitting pipeline test_model_pca_1'),
                    mock.call('Accuracy for test_model_pca_1: 100.0%'),
                    mock.call('It took 0.0 seconds to train test_model_pca_1 pipeline.'),
                    mock.call('The best pipe was test_model_pca_1 with an accuracy of: 100.0%'),
                    mock.call(f'Best pipeline saved in {TRAINED_FILE_PATH}best_pipe.pkl'),
                    mock.call('It took 0.0 seconds to train all the pipelines.')
                ]
            )
