import pandas as pd

from brain_services.transformers import BaseTransformer


class CleanNanValuesTransformer(BaseTransformer):
    """
    This transformer will clean all Nan values using the strategy you choose, for example dropna, replace, fillna...
    with the arguments you specify
    """

    strategy: str = None
    strategy_kwargs: dict = None

    def __init__(
        self,
        strategy: str = 'dropna',
        strategy_kwargs=None
    ):
        """

        :param strategy: The method of dataframe to use to clean it, by default is dropna
        :param strategy_kwargs: The arguments of the method to use, by default is {'inplace': True}
        """

        # Avoid default argument mutable
        if strategy_kwargs is None:
            strategy_kwargs = {'inplace': True}
        self.strategy = strategy
        self.strategy_kwargs = strategy_kwargs

    def transform(self, x: pd.DataFrame, y: pd.DataFrame = None):
        getattr(x, self.strategy)(**self.strategy_kwargs)
        return x
