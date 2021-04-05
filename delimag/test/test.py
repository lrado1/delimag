# Any changes to the distributions library should be reinstalled with
#  pip install --upgrade .

# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest
import pandas as pd
import numpy as np

from delimag import Delimag

# Open data for testing
test_df = pd.read_csv('test_data.csv')

class TestDelimagClass(unittest.TestCase):
    
    def setUp(self):
        self.delimag = Delimag2d(test_df, 'Object', 'Color', 'Value')
    
 
    
    
    def test_initialization(self):
        self.assertEqual(self.delimag.var_group, 'Object', "var_vertical initialized incorrectly")
        self.assertEqual(self.delimag.var_subgroup, 'Color', "var_horizontal initialized incorrectly")
        self.assertEqual(self.delimag.var_value, 'Value', "var_value initialized incorrectly")
        self.assertEqual(self.delimag.result, [], "result attribute initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[0,'Object'], "Cube;Pyramid;Cone", "data initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[10,'Color'], "Black;Black;Blue", "data initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[19,'Value'], 11.0, "data initialized incorrectly")   
    
    
    
    
    def distinct_vertical(self):
        self.assertSequenceEqual(self.delimag.distinct_values(), ['Cube', 'Pyramid', 'Cone', 'Sphere'], 
                         ".distinct_values() returned incorrect list of values")
        
        self.assertSequenceEqual(self.delimag.distinct_values(dropna=False), ['Cube', 'nan', 'Sphere', 'Pyramid', 'Cone'],
                         ".distinct_values() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', drop_na=False)[1], 'Cube;Pyramid', 
                         ".distinct_values() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', drop_na=False)[5], 'Sphere;Pyramid', 
                         ".distinct_values() returned incorrect list of values")
    
    
    
    
    def distinct_horizontal(self):
        self.assertSequenceEqual(self.delimag.distinct_values(switch_group=True), ['Black', 'Blue', 'Red', 'Green'], 
                         ".distinct_values() returned incorrect list of values")
        
        self.assertSequenceEqual(self.delimag.distinct_values(dropna=False, switch_group=True), ['Black', 'nan', 'Blue', 'Red', 'Green'],
                         ".distinct_values() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', drop_na=False, switch_group=True)[1], 'Black;Red', 
                         ".distinct_values() returned incorrect value")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', drop_na=False, switch_group=True)[5], 'Green;Blue;Blue', 
                         ".distinct_values() returned incorrect value")
    
    
    
    
    def aggregate(self):
        self.assertEqual(self.delimag.aggregate().loc['Black', 'Cone'], 3,
                          ".aggregate() returned incorrect count value")
        
        self.assertEqual(self.delimag.aggregate(calc=len).loc['Black', 'Cone'], 3,
                          ".aggregate() returned incorrect count value")
        
        self.delimag.aggregate(calc=len)
        self.assertEqual(self.delimag.result.loc['Black', 'Cone'], 3,
                          ".aggregate() updated result class attribute incorrectly")
        
        self.assertAlmostEqual(self.delimag.aggregate(calc=np.mean).loc['Black', 'Cone'], 63.333333, 
                          ".aggregate() returned incorrect mean value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.sum).loc['Blue', 'Pyramid'], 0, 
                          ".aggregate() returned incorrect sum value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.min).loc['Red', 'Pyramid'], 43, 
                          ".aggregate returned incorrect min value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.min).loc['Green', 'Cone'], 24.0, 
                          ".aggregate returned incorrect min value")
    
        self.assertEqual(self.delimag.aggregate(calc=np.max).loc['Black', 'Cone'], 96, 
                          ".aggregate returned incorrect max value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.max).loc['Black', 'Sphere'], 49, 
                          ".aggregate returned incorrect max value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.max, delim_vertical=' ', delim_horizontal=' ').loc['Black;Red', 'Cone;Pyramid'], 43, 
                          ".aggregate returned incorrect calc value when delim=' '")
    
    
    
    
    def return_result(self):
        self.delimag.aggregate(calc=len)
        self.assertEqual(self.return_result().loc['Black', 'Cone'], 3,
                          ".return_result() method returned incorrec value")
        
        self.assertEqual(self.return_result(sort_by_vertical='Cone').iloc[1,1], 1,
                          "result class attribute returned incorrec value")
        
        self.assertEqual(self.return_result(sort_by_vertical='Pyramid').iloc[3,2], 3,
                          "result class attribute returned incorrec value")
        
        self.delimag.aggregate_cross(calc=np.sum)
        self.assertEqual(self.return_result(sort_by_vertical='Pyramid', sort_by_horizontal='Green').iloc[2,2], 114.0,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.return_result(sort_by_vertical='Pyramid', 
                                                  sort_by_horizontal='Green', 
                                                  proportionize='column').loc[:,'Sphere'].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.return_result(sort_by_vertical='Pyramid', 
                                                  sort_by_horizontal='Green', 
                                                  proportionize='column').loc[:,'Cube'].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.return_result(sort_by_vertical='Pyramid', 
                                                  sort_by_horizontal='Green', 
                                                  proportionize='column').loc[:,'Cone'].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.return_result(sort_by_vertical='Pyramid', 
                                            sort_by_horizontal='Green', 
                                            proportionize='row').loc['Black',:].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.return_result(sort_by_vertical='Pyramid', 
                                            sort_by_horizontal='Green', 
                                            proportionize='row').loc['Blue',:].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.return_result(sort_by_vertical='Pyramid', 
                                            sort_by_horizontal='Green', 
                                            proportionize='row').loc['Red',:].sum(), 1,
                          "result class attribute returned incorrec value")
        
        
        self.assertAlmostEqual(self.return_result(sort_by_vertical='Pyramid', 
                                            sort_by_horizontal='Green', 
                                            proportionize='total').loc['Red',:].sum(), 0.4507501630789302,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.return_result(proportionize='total').loc['Red',:].sum(), 0.4507501630789302,
                          "result class attribute returned incorrec value")
        