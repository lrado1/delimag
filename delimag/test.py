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
                         ".distinct_horizontal() returned incorrect value")
        
        self.assertEqual(self.delimag.distinct_horizontal(delim=' ', drop_na=False)[5], 'Green;Blue;Blue', 
                         ".distinct_horizontal() returned incorrect value")
    
    
    def aggregate_vertical(self):
        
        self.assertEqual(self.delimag.aggregate_vertical().loc['Cube'][0], 8,
                          ".aggregate_vertical() returned incorrect count value")
        
        self.assertEqual(self.delimag.aggregate_vertical(calc='count').loc['Cube'][0], 8,
                          ".aggregate_vertical() returned incorrect count value")
        
        self.delimag.aggregate_vertical(calc='count')
        self.assertEqual(self.delimag.result.loc['Cube'][0], 8,
                          ".aggregate_vertical() updated result class attribute incorrectly")
        
        self.assertAlmostEqual(self.delimag.aggregate_vertical(calc='mean').loc['Cube'][0], 51.428571, 
                          ".aggregate_vertical() returned incorrect mean value")
        
        self.assertEqual(self.delimag.aggregate_vertical(calc='sum').loc['Cube'][0], 360, 
                          ".aggregate_vertical() returned incorrect sum value")
        
        self.assertEqual(self.delimag.aggregate_vertical(calc='min').loc['Cube'][0], 12, 
                          ".aggregate_vertical() returned incorrect min value")
        
        self.assertEqual(self.delimag.aggregate_vertical(calc='min').loc['Sphere'][0], 17, 
                          ".aggregate_vertical() returned incorrect min value")
    
        self.assertEqual(self.delimag.aggregate_vertical(calc='max').loc['Cone'][0], 96, 
                          ".aggregate_vertical() returned incorrect max value")
        
        self.assertEqual(self.delimag.aggregate_vertical(calc='max').loc['Pyramid'][0], 90, 
                          ".aggregate_vertical() returned incorrect max value")
        
        self.assertEqual(self.delimag.aggregate_vertical(calc='count', delim=' ').loc['Sphere'][0], 5, 
                          ".aggregate_vertical() returned incorrect calc value when delim=' '")
        


        
    def aggregate_horizontal(slef):
        self.assertEqual(self.delimag.aggregate_horizontal().loc['Black'][0], 9,
                          ".aggregate_horizontal() returned incorrect count value")
        
        self.assertEqual(self.delimag.aggregate_horizontal(calc='count').loc['Black'][0], 9,
                          ".aggregate_horizontal() returned incorrect count value")
        
        self.delimag.aggregate_horizontal(calc='count')
        self.assertEqual(self.delimag.result.loc['Black'][0], 9,
                          ".aggregate_horizontal() updated result class attribute incorrectly")
        
        self.assertAlmostEqual(self.delimag.aggregate_horizontal(calc='mean').loc['Black'][0], 62.77777777777778, 
                          ".aggregate_horizontal() returned incorrect mean value")
        
        self.assertEqual(self.delimag.aggregate_horizontal(calc='sum').loc['Black'][0], 565.0, 
                          ".aggregate_horizontal() returned incorrect sum value")
        
        self.assertEqual(self.delimag.aggregate_horizontal(calc='min').loc['Black'][0], 12.0, 
                          ".aggregate_horizontal() returned incorrect min value")
        
        self.assertEqual(self.delimag.aggregate_horizontal(calc='min').loc['Green'][0], 24.0, 
                          ".aggregate_horizontal() returned incorrect min value")
    
        self.assertEqual(self.delimag.aggregate_horizontal(calc='max').loc['Red'][0], 63, 
                          ".aggregate_horizontal() returned incorrect max value")
        
        self.assertEqual(self.delimag.aggregate_horizontal(calc='max').loc['Blue'][0], 96, 
                          ".aggregate_horizontal() returned incorrect max value")
        
        self.assertEqual(self.delimag.aggregate_horizontal(calc='count', delim=' ').loc['Black'][0], 9, 
                          ".aggregate_horizontal() returned incorrect calc value when delim=' '")
    
    
    
    
    def aggregate_cross(self):
        pass
    
    def return_result(self):
        pass