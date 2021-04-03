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
    
    def test_initialization(self):
        self.assertEqual(self.delimag.var_vertical, 'Object', "var_vertical initialized incorrectly")
        self.assertEqual(self.delimag.var_horizontal, 'Color', "var_horizontal initialized incorrectly")
        self.assertEqual(self.delimag.var_value, 'Value', "var_value initialized incorrectly")
        self.assertEqual(self.delimag.result, [], "result attribute initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[0,'Object'], "Cube;Pyramid;Cone", "data initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[10,'Color'], "Black;Black;Blue", "data initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[19,'Value'], 11.0, "data initialized incorrectly")   
    
    def distinct_vertical(self):
        self.assertSequenceEqual(self.delimag.distinct_vertical(), ['Cube', 'Pyramid', 'Cone', 'Sphere'], 
                         ".distinct_vertical() returned incorrect list of values")
        
        self.assertSequenceEqual(self.delimag.distinct_vertical(dropna=False), ['Cube', 'nan', 'Sphere', 'Pyramid', 'Cone'],
                         ".distinct_vertical() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_vertical(delim=' ', drop_na=False)[1], 'Cube;Pyramid', 
                         ".distinct_vertical() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_vertical(delim=' ', drop_na=False)[5], 'Sphere;Pyramid', 
                         ".distinct_vertical() returned incorrect list of values")
    
    
    def distinct_horizontal(self):
        self.assertSequenceEqual(self.delimag.distinct_horizontal(), ['Black', 'Blue', 'Red', 'Green'], 
                         ".distinct_horizontal() returned incorrect list of values")
        
        self.assertSequenceEqual(self.delimag.distinct_horizontal(dropna=False), ['Black', 'nan', 'Blue', 'Red', 'Green'],
                         ".distinct_horizontal() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_horizontal(delim=' ', drop_na=False)[1], 'Black;Red', 
                         ".distinct_horizontal() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_horizontal(delim=' ', drop_na=False)[5], 'Green;Blue;Blue', 
                         ".distinct_horizontal() returned incorrect list of values")
    
    
    def aggregate_vertical(self):
        pass
        
    def aggregate_horizontal(slef):
        pass
    
    def aggregate_cross(self):
        pass
    
    def return_result(self):
        pass