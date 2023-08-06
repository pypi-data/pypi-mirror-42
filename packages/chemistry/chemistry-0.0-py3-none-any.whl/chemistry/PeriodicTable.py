import os
import pandas as pd
from copy import deepcopy

from .helpers.standardize_columns import standardize_columns

my_path = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(my_path, 'data_files')
periodic_table_path = os.path.join(data_dir, 'periodic_table.csv')

PERIODIC_TABLE = standardize_columns(data=pd.read_csv(periodic_table_path))


class PeriodicTable:
	def __init__(self):
		self._data = PERIODIC_TABLE

	@property
	def data(self):
		return deepcopy(self._data)



