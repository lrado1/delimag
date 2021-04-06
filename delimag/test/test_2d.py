# For running unit tests, first import the Delimag1d and Delimag2d package
# Than run this python script from terminal

import unittest
import pandas as pd
import numpy as np


# Open data for testing
test_df = pd.read_csv('test_data.csv')

class TestDelimag2dClass(unittest.TestCase):
    
    def setUp(self):
        self.delimag = Delimag2d(test_df, 'Object', 'Color', 'Value')
        
    def test_bool_parameters_raise_error(self):
        
        self.delimag.aggregate(calc=len)
        self.assertEqual(self.delimag.return_result().loc['Black', 'Cone'], 3,
                          ".return_result() method returned incorrec value")
        
        with self.assertRaises(ValueError):
            self.delimag.distinct_values(dropna='x')
            
        with self.assertRaises(ValueError):
            self.delimag.distinct_values(switch_group='x')
            
        with self.assertRaises(ValueError):
            self.delimag.aggregate(dropna_vertical='x')
            
        with self.assertRaises(ValueError):
            self.delimag.aggregate(dropna_horizontal='x')
        
        with self.assertRaises(ValueError):
            self.delimag.aggregate(dropna_value='x')
            
        with self.assertRaises(ValueError):
            self.delimag.aggregate(show_results='x')
            
        with self.assertRaises(ValueError):
            self.delimag.return_result(proportionize='X')
            
            
    
    def test_initialization(self):
        self.assertEqual(self.delimag.var_group, 'Object', "var_vertical initialized incorrectly")
        self.assertEqual(self.delimag.var_subgroup, 'Color', "var_horizontal initialized incorrectly")
        self.assertEqual(self.delimag.var_value, 'Value', "var_value initialized incorrectly")
        self.assertEqual(self.delimag.result, [], "result attribute initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[0,'Object'], "Cube;Pyramid;Cone", "data initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[10,'Color'], "Black;Black;Blue", "data initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[19,'Value'], 11.0, "data initialized incorrectly")   
    
    
    
    
    def test_distinct_vertical(self):
        self.assertSequenceEqual(self.delimag.distinct_values(), ['Cube', 'Pyramid', 'Cone', 'Sphere'], 
                         ".distinct_values() returned incorrect list of values")
        
        self.assertSequenceEqual(self.delimag.distinct_values(dropna=False), ['Cone', 'nan', 'Pyramid', 'Sphere', 'Cube'],
                         ".distinct_values() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', dropna=False)[1], 'Pyramid;Sphere', 
                         ".distinct_values() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', dropna=False)[5], 'Cone;Pyramid', 
                         ".distinct_values() returned incorrect list of values")
    
    
    
    
    def test_distinct_horizontal(self):
        self.assertSequenceEqual(self.delimag.distinct_values(switch_group=True), ['Red', 'Black', 'Blue', 'Green'], 
                         ".distinct_values() returned incorrect list of values")
        
        self.assertSequenceEqual(self.delimag.distinct_values(dropna=False, switch_group=True), ['nan', 'Red', 'Black', 'Green', 'Blue'],
                         ".distinct_values() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', dropna=False, switch_group=True)[0], 'Blue;Blue', 
                         ".distinct_values() returned incorrect value")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', dropna=False, switch_group=True)[12], 'Green;Blue;Blue', 
                         ".distinct_values() returned incorrect value")
    
    
    
    
    def test_aggregate(self):
        self.assertEqual(self.delimag.aggregate().loc['Black', 'Cone'], 3,
                          ".aggregate() returned incorrect count value")
        
        self.assertEqual(self.delimag.aggregate(calc=len).loc['Black', 'Cone'], 3,
                          ".aggregate() returned incorrect count value")
        
        self.delimag.aggregate(calc=len)
        self.assertEqual(self.delimag.result.loc['Black', 'Cone'], 3,
                          ".aggregate() updated result class attribute incorrectly")
        
        self.assertAlmostEqual(self.delimag.aggregate(calc=np.mean).loc['Black', 'Cone'], 63.333333, 6, 
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
    
    
    
    
    def test_return_result(self):
        self.delimag.aggregate(calc=len)
        self.assertEqual(self.delimag.return_result().loc['Black', 'Cone'], 3,
                          ".return_result() method returned incorrec value")
        
        self.assertEqual(self.delimag.return_result(sort_by_vertical='Cone').iloc[1,1], 1,
                          "result class attribute returned incorrec value")
        
        self.assertEqual(self.delimag.return_result(sort_by_vertical='Pyramid').iloc[3,2], 3,
                          "result class attribute returned incorrec value")
        
        self.delimag.aggregate(calc=np.sum)
        self.assertEqual(self.delimag.return_result(sort_by_vertical='Pyramid', sort_by_horizontal='Green').iloc[2,2], 114.0,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.delimag.return_result(sort_by_vertical='Pyramid', 
                                                  sort_by_horizontal='Green', 
                                                  proportionize='column').loc[:,'Sphere'].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.delimag.return_result(sort_by_vertical='Pyramid', 
                                                  sort_by_horizontal='Green', 
                                                  proportionize='column').loc[:,'Cube'].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.delimag.return_result(sort_by_vertical='Pyramid', 
                                                  sort_by_horizontal='Green', 
                                                  proportionize='column').loc[:,'Cone'].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.delimag.return_result(sort_by_vertical='Pyramid', 
                                            sort_by_horizontal='Green', 
                                            proportionize='row').loc['Black',:].sum(), 1, 6,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.delimag.return_result(sort_by_vertical='Pyramid', 
                                            sort_by_horizontal='Green', 
                                            proportionize='row').loc['Blue',:].sum(), 1,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.delimag.return_result(sort_by_vertical='Pyramid', 
                                            sort_by_horizontal='Green', 
                                            proportionize='row').loc['Red',:].sum(), 1,
                          "result class attribute returned incorrec value")
        
        
        self.assertAlmostEqual(self.delimag.return_result(sort_by_vertical='Pyramid', 
                                            sort_by_horizontal='Green', 
                                            proportionize='total').loc['Red',:].sum(), 0.16634050880626222, 7,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.delimag.return_result(proportionize='total').loc['Red',:].sum(), 0.16634050880626222, 7,
                          "result class attribute returned incorrec value")

        
        
        

        
        
        
        
tests = TestDelimag2dClass()
test_loaded  = unittest.TestLoader().loadTestsFromModule(tests)
unittest.TextTestRunner().run(test_loaded)