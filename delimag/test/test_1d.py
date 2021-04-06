# For running unit tests, first import the Delimag1d and Delimag2d package
# Than run this python script from terminal

import unittest
import pandas as pd
import numpy as np


# Open data for testing
test_df = pd.read_csv('test_data.csv')

class TestDelimag1dClass(unittest.TestCase):
    
    def setUp(self):
        self.delimag = Delimag1d(test_df, 'Object', 'Value')
    
    def test_initialization(self):
        self.assertEqual(self.delimag.var_group, 'Object', "var_vertical initialized incorrectly")
        self.assertEqual(self.delimag.var_value, 'Value', "var_value initialized incorrectly")
        self.assertEqual(self.delimag.result, [], "result attribute initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[0,'Object'], "Cube;Pyramid;Cone", "data initialized incorrectly")
        self.assertEqual(self.delimag.data.loc[19,'Value'], 11.0, "data initialized incorrectly")   
    
    
    
    
    def test_distinct_values(self):
        self.assertSequenceEqual(self.delimag.distinct_values(), ['Cube', 'Pyramid', 'Cone', 'Sphere'], 
                         ".distinct_values() returned incorrect list of values")
        
        self.assertSequenceEqual(self.delimag.distinct_values(dropna=False), ['Cone', 'nan', 'Pyramid', 'Sphere', 'Cube'],
                         ".distinct_values() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', dropna=False)[1], 'Pyramid;Sphere', 
                         ".distinct_values() returned incorrect list of values")
        
        self.assertEqual(self.delimag.distinct_values(delim=' ', dropna=False)[5], 'Cone;Pyramid', 
                         ".distinct_values() returned incorrect list of values")
        
    
    
    
    def test_aggregate(self):
        self.assertEqual(self.delimag.aggregate().loc['Cone'], 7,
                          ".aggregate() returned incorrect count value")
        
        self.assertEqual(self.delimag.aggregate(calc=len).loc['Cone'], 7,
                          ".aggregate() returned incorrect count value")
        
        self.delimag.aggregate(calc=len)
        self.assertEqual(self.delimag.result.loc['Cone'], 7,
                          ".aggregate() updated result class attribute incorrectly")
        
        self.assertAlmostEqual(self.delimag.aggregate(calc=np.mean).loc['Cone'], 52.5, 6, 
                          ".aggregate() returned incorrect mean value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.sum).loc['Pyramid'], 356, 
                          ".aggregate() returned incorrect sum value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.min).loc['Pyramid'], 17, 
                          ".aggregate returned incorrect min value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.min).loc['Cone'], 11, 
                          ".aggregate returned incorrect min value")
    
        self.assertEqual(self.delimag.aggregate(calc=np.max).loc['Cone'], 96, 
                          ".aggregate returned incorrect max value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.max).loc['Sphere'], 53, 
                          ".aggregate returned incorrect max value")
        
        self.assertEqual(self.delimag.aggregate(calc=np.max, delim_vertical=' ', delim_horizontal=' ').loc['Cone;Pyramid'], 43, 
                          ".aggregate returned incorrect calc value when delim=' '")
    
    
    
    
    def test_return_result(self):
        self.delimag.aggregate(calc=len)
        self.assertEqual(self.delimag.return_result().loc['Cone'], 7,
                          ".return_result() method returned incorrec value")
        
        self.assertEqual(self.delimag.return_result(sort_by='index').iloc[1,1][0], 7,
                          "result class attribute returned incorrec value")
        
        self.assertEqual(self.delimag.return_result(sort_by='len').iloc[3][0], 9,
                          "result class attribute returned incorrec value")
        
        self.delimag.aggregate(calc=[len, np.sum, np.mean])
        self.assertAlmostEqual(self.delimag.return_result(sort_by='index').iloc[2,2], 50.857142857142854, 7,
                          "result class attribute returned incorrec value")
        
        self.delimag.aggregate(calc=[len, np.sum, np.mean], dropna_value=True)
        self.assertEqual(self.delimag.return_result(sort_by='index').iloc[1,1], 6,
                          "result class attribute returned incorrec value")
        
        
        self.assertAlmostEqual(self.delimag.return_result(sort_by='len', proportionize=True).loc[:,'len'].sum(), 1, 7,
                          "result class attribute returned incorrec value")
        
        self.assertAlmostEqual(self.delimag.return_result(
                    sort_by='len', proportionize=True).loc['Cone'].sum(),0.779506591245881, 7,
                          "result class attribute returned incorrec value")
    
    
    
    
    def test_bool_parameters_raise_error(self):
        self.delimag = Delimag1d(test_df, 'Object', 'Value')
        
        with self.assertRaises(ValueError):
            self.self.delimag = Delimag1d(test_df, 'Object', 'Value')
            
        with self.assertRaises(ValueError):
            self.delimag.aggregate(dropna_value='x')
        
        with self.assertRaises(ValueError):
            self.delimag.aggregate(dropna_group='x')
            
        with self.assertRaises(ValueError):
            self.delimag.return_result(ascending='x')
        
        with self.assertRaises(ValueError):
            self.delimag.return_result(proportionize='x')
            
        with self.assertRaises(ValueError):
            self.delimag.distinct_values(dropna='x')
        
        
        
tests = TestDelimagClass()
test_loaded  = unittest.TestLoader().loadTestsFromModule(tests)
unittest.TextTestRunner().run(test_loaded)