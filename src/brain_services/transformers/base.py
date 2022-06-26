import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class BaseTransformer(BaseEstimator, TransformerMixin):
    """
    Base transformer that inherit from the needed objects for the pipeline.

    This class is abstract, so it can not be instanced.
    """

    class Meta:
        abstract = True

    def fit(self, x: pd.DataFrame, y: pd.DataFrame = None):
        # print(f'{self.__class__.__name__} called with x: {list(x.keys())}\n\n\n')
        return self

    def transform(self, x: pd.DataFrame, y: pd.DataFrame = None):
        raise NotImplementedError()
