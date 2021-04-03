# Any changes to the distributions library should be reinstalled with
#  pip install --upgrade .

# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest
import pandas as pd

from delimag import Delimag


# Open data for testing
test_df = pd.read_csv('test_data.csv')

class TestDelimagClass(unittest.TestCase):
    def setUp(self):
        self.delimag = Delimag(test_df, 'Object', 'Color', 'Value')
    
    def distinct_vertical()
    
    
    
    distinct_horizontal
    
    
    aggregate_vertical
    
    
    aggregate_horizontal
    
    
    aggregate_cross
    
    
    return_result
    
    
    