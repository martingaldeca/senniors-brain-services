import pandas as pd

from brain_services.transformers import BaseTransformer


class TesBaseTransformerMixin:
    transformer: BaseTransformer = None

    input_data_frame_dict: dict = None
    output_data_frame_dict: dict = None
    initial_column_names: list = None
    final_column_names: list = None
    init_kwargs: dict = None
    input_data_frame: pd.DataFrame = None
    output_data_frame: pd.DataFrame = None

    def setUp(self):
        if not self.final_column_names:
            self.final_column_names = self.initial_column_names
        self.input_data_frame = pd.DataFrame.from_dict(
            self.input_data_frame_dict,
            orient='index',
            columns=self.initial_column_names
        )
        self.output_data_frame = pd.DataFrame.from_dict(
            self.output_data_frame_dict,
            orient='index',
            columns=self.final_column_names
        )

    def test_transform(self):
        transformer = self.transformer(**self.init_kwargs)
        self.assertTrue(pd.DataFrame.equals(transformer.transform(x=self.input_data_frame), self.output_data_frame))
