import logging
import typing

import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


class DataLoader:
    """
    This object is in charge of load the data from the original csv and split the data into 2 dataframes,
    1 for testing and 1 for training, also can split the data using a balancer (RandomUnderSampler) in order to have
    the same positive and negative values in the training
    """
    data_path: str = None
    test_size: float = None
    balanced_data: bool = None
    y_column_name: str = ''
    random_state: int = None

    df: pd.DataFrame = None
    x: pd.DataFrame = None
    y: pd.DataFrame = None

    train_df: pd.DataFrame = None
    test_df: pd.DataFrame = None

    train_x_df: pd.DataFrame = None
    train_y_df: pd.DataFrame = None
    test_x_df: pd.DataFrame = None
    test_y_df: pd.DataFrame = None

    def __init__(
        self,
        data_path: str = './data/senniorhealth_patients.csv',
        test_size: float = 0.2,
        balanced_data: bool = False,
        y_column_name: str = 'No-show',
        random_state: typing.Optional[int] = None,
    ):
        """

        :param data_path: Path of the main csv
        :param test_size: Value that determines the % of test data and training data
        :param balanced_data: Boolean that indicates if the data will be balanced
        :param y_column_name: Name of the results' column
        :param random_state: Value for random state of the RandomUnderSampler
        """
        # Save the object fields
        self.data_path = data_path
        self.test_size = test_size
        self.balanced_data = balanced_data
        self.y_column_name = y_column_name
        self.random_state = random_state

        # Load data
        try:
            self.df = pd.read_csv(self.data_path)
        except FileNotFoundError as ex:
            logger.error('Not valid data path', extra={'data_path': self.data_path})
            raise ex
        except pd.errors.ParserError as ex:
            logger.error('Not valid format for file, it must be a csv', extra={'data_path': self.data_path})
            raise ex

        # Validate the other parameters
        self._validate_parameters(
            test_size=test_size,
            balanced_data=balanced_data,
            y_column_name=y_column_name,
        )

        # Split input and output
        self.x = self.df.loc[:, self.df.columns != self.y_column_name]
        self.y = self.df[self.y_column_name]

        # Check if we want to train the model with balanced data
        self._update_df_to_use()

        # Split the data
        self._train_test_split()

    def _update_df_to_use(self):
        """
        Method to balance the data in order to have the same negative and positive values for result column during the
        training
        :return: None
        """
        self.df_to_use = self.df
        if self.balanced_data:
            rus = RandomUnderSampler(random_state=self.random_state)
            self.x, self.y = rus.fit_resample(self.x, self.y)
            self.df_to_use = self.x.assign(**{self.y_column_name: self.y})

    def _train_test_split(self):
        """
        Split the data in 2 different dataframes, 1 for training and 1 for testing
        :return:
        """
        self.train_df, self.test_df = train_test_split(
            self.df_to_use,
            test_size=self.test_size,
            random_state=self.random_state
        )
        self.train_x, self.train_y = (
            self.train_df.loc[:, self.train_df.columns != self.y_column_name],
            self.train_df[self.y_column_name]
        )
        self.test_x, self.test_y = (
            self.test_df.loc[:, self.test_df.columns != self.y_column_name],
            self.test_df[self.y_column_name]
        )

    def _validate_parameters(
        self,
        test_size: float,
        balanced_data: bool,
        y_column_name: str,
    ):
        """
        Validate the parameters of the dataloader

        :param test_size: Must be between 0 and 1
        :param balanced_data: Must be a boolean value
        :param y_column_name: Must be one of the column names of the main data frame
        :return: None
        """
        if test_size < 0 or test_size > 1:
            raise ValueError(f'Test size not valid, must be between 0 and 1, not "{test_size}"')
        if type(balanced_data) != bool:
            raise ValueError(f'Balanced data not valid, must be True or False, not "{balanced_data}"')
        if y_column_name not in self.df.columns:
            raise ValueError(f'Y column name "{y_column_name}" is not a valid column name')
