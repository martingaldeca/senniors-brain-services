import logging
import os.path

import joblib

from settings import TRAINED_FILE_PATH

logger = logging.getLogger(__name__)


class SenniorsPredictor:
    """
    The predictor is an interface of the trained pipe that returns a value that the service can send
    """
    trained_pipe_file_path: str = None
    pipe = None

    def __init__(
        self,
        trained_pipe_file_path: str = f'{TRAINED_FILE_PATH}best_pipe.pkl'
    ):
        """
        Load the pipeline to use, check that exists a previous trained pipe, if not it will raise an error
        """
        self.trained_pipe_file_path = trained_pipe_file_path
        if not os.path.exists(self.trained_pipe_file_path):
            raise ValueError(f'"{self.trained_pipe_file_path}" is not a valid trained pipe file')
        self.pipe = joblib.load(f'{TRAINED_FILE_PATH}best_pipe.pkl')

    def predict(self, x):
        """
        This method calls the predict method of the pipeline and interprets the result
        :param x: Inputted data
        :return: bool That shows if the customer will attend to the hospital (True) or not (False)
        """
        try:
            prediction = self.pipe.predict(x)
        except Exception as ex:
            logger.error(
                'There was a problem with the prediction',
                extra={
                    'x': x,
                }
            )
            raise ex
        logger.debug(f'The prediction was "{prediction}", input data was "{x}"')
        attending = prediction[0] == 'No'
        return attending
