class Delimag():
    """
    Delimag is a tool to analyze Pandas DataFrame objects with multiselect records.
        
        
    Attributes:


    Methods:

            
    """

    def __init__(self, data, var_vertical, var_horizontal="", var_value=""):
        self.data = data
        self.var_vertical = var_vertical
        self.var_horizontal = var_horizontal
        self.var_value = var_value
        self._aggregation_type = ''
        self._aggregation_method = ''
    
    
    
    def __version__():
        pass
    
    
    
    def __repr__(self):
        
        df_name =[x for x in globals() if globals()[x] is self.data][0]
        
        return (f'DataFrame name: {df_name} \n'
                f'Vertical variable: {self.var_vertical} \n'
                f'Horizontal variable: {self.var_horizontal} \n'
                f'Value variable: {self.var_value} \n'
                f'Aggregation type: {self._aggregation_type} \n'
                f'Aggregation method: {self._aggregation_method}')     
    
    
    
    def distinct_vertical(self, delim=';', drop_na=True):
        """
        Return a list of distinct values from the col_vertical variable, after splitting the delimited records.
        """
         
        
        
    def distinct_horizontal(self, delim=';', drop_na=True):
        """
        Return a list of distinct values from the col_horizontal variable, after splitting the delimited records.
        """
       
        
    
    def aggregate_vertical(self, calc='count', delim=';', drop_na=True):
        """
        Aggregate along the col_vertical variable.
        """
    
    
    
    
    def aggregate_horizontal(self, calc='count', delim=';', drop_na=True):
        """
        Aggregate along the col_horizontal variable.
        """
        
                
            
    def aggregate_cross(self, calc='count', delim_vertical=';', delim_horizontal=';'):
        """
        Create a cross-tabulation based on two variables and aggregates a third variables's values based on the cross-groupping.
        """
        
        
    def condition(self, vertical, horizontal, value):
        """
        Filter the result set of the aggregation. 
        """

        
        
    def result(self, sort_vertical, sort_horizontal, proportionize=False):
        """
        Return the result set of the aggregation in a Pandas DataFrame object in an organized format (sorted, proportionized).
        """
        
        