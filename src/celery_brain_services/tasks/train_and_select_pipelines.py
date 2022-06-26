import logging
import time
import logging.config
from typing import List

import joblib
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from imblearn.pipeline import Pipeline

from brain_services.data_loader import DataLoader
from celery_brain_services.tasks.settings import (
    BASE_STEPS, MODELS_TO_USE_LIST,
    PCA_OPTIMIZATION_COMPONENTS,
)
from settings import TRAINED_FILE_PATH

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def train_and_select_pipelines():
    start = time.process_time()
    data_loader = DataLoader()
    pipelines: List[List[str, Pipeline]] = []
    models_to_use_list = MODELS_TO_USE_LIST
    base_steps = BASE_STEPS
    for pca_optimization_components in PCA_OPTIMIZATION_COMPONENTS:
        steps_to_use = base_steps.copy()
        if pca_optimization_components:
            steps_to_use.append(
                (
                    f'pca_optimization_with_{pca_optimization_components}_components',
                    PCA(n_components=pca_optimization_components)
                )
            )
        for model_to_use in models_to_use_list:
            model_steps_to_use = steps_to_use.copy()
            model_steps_to_use.append(model_to_use)

            pipelines.append(
                [
                    f'{model_to_use[0]}_pca_{pca_optimization_components}',
                    Pipeline(
                        steps=model_steps_to_use
                    ),
                ]
            )
    best_pipe_name = None
    best_pipe = None
    best_pipe_scoring = 0
    for pipe_name, pipe in pipelines:
        start_time_for_pipe = time.process_time()
        logger.info(f'Fitting pipeline {pipe_name}')
        pipe.fit(data_loader.train_x, data_loader.train_y)
        scores = cross_val_score(
            pipe,
            data_loader.train_x,
            data_loader.train_y,
            cv=15,
            scoring='accuracy'
        )
        pipe_score = round(scores.mean(), 4)
        logger.info(f'Accuracy for {pipe_name}: {round(pipe_score * 100, 2)}%')
        logger.info(
            f'It took {round(time.process_time() - start_time_for_pipe, 4)} seconds to train {pipe_name} pipeline.'
        )
        if pipe_score >= best_pipe_scoring:
            best_pipe_name = pipe_name
            best_pipe = pipe
            best_pipe_scoring = pipe_score

    logger.info(f'The best pipe was {best_pipe_name} with an accuracy of: {round(best_pipe_scoring * 100, 2)}%')
    # Save the best pipeline
    joblib.dump(best_pipe, f'{TRAINED_FILE_PATH}best_pipe.pkl')
    logger.info(f'Best pipeline saved in {TRAINED_FILE_PATH}best_pipe.pkl')
    logger.info(f'It took {round(time.process_time() - start, 4)} seconds to train all the pipelines.')
