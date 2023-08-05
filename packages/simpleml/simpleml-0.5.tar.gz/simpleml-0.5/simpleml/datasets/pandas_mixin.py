'''
Pandas Module for external dataframes

Inherit and extend for particular patterns. It is a bit of a misnomer to use the
term "dataframe", since there are very few expected attributes and they are by no
means unique to pandas.
'''

__author__ = 'Elisha Yadgaran'

from simpleml import TRAIN_SPLIT
from simpleml.datasets.abstract_mixin import AbstractDatasetMixin
import pandas as pd

DATAFRAME_SPLIT_COLUMN = 'DATASET_SPLIT'


class PandasDatasetMixin(AbstractDatasetMixin):
    @property
    def X(self):
        '''
        Return the subset that isn't in the target labels
        '''
        return self.dataframe[self.dataframe.columns.difference(self.label_columns)]

    @property
    def y(self):
        '''
        Return the target label columns
        '''
        return self.dataframe[self.label_columns]

    def get(self, column, split):
        '''
        Explicitly split validation splits
        Assumes self.dataframe has a get method to return the dataframe associated with the split
        Uses self.label_columns to separate x and y columns inside the returned dataframe
        '''
        if column not in ('X', 'y'):
            raise ValueError('Only support columns: X & y')

        if isinstance(self.dataframe, pd.DataFrame):
            df = self.dataframe.query("{}=='{}'".format(DATAFRAME_SPLIT_COLUMN, split))
            df.drop(DATAFRAME_SPLIT_COLUMN, inplace=True, axis=1)
        else:
            df = self.dataframe.get(split)
        if df is None:
            df = pd.DataFrame()

        if column == 'y':
            return df[[col for col in self.label_columns if col in df.columns]]

        else:
            return df[df.columns.difference(self.label_columns)]

    def concatenate_dataframes(self, dataframes, splits):
        '''
        Helper method to merge dataframes into a single one with the split
        specified under `DATAFRAME_SPLIT_COLUMN`
        '''
        for df, split in zip(dataframes, splits):
            df[DATAFRAME_SPLIT_COLUMN] = split

        return pd.concat(dataframes)

    def get_feature_names(self):
        '''
        Should return a list of the features in the dataset
        '''
        try:
            return self.X.columns.tolist()
        except AttributeError:
            return self.get('X', TRAIN_SPLIT).columns.tolist()

    @staticmethod
    def load_csv(filename, **kwargs):
        '''Helper method to read in a csv file'''
        return pd.read_csv(filename, **kwargs)

    @staticmethod
    def load_sql(query, connection, **kwargs):
        '''Helper method to read in sql data'''
        return pd.read_sql_query(query, connection, **kwargs)
