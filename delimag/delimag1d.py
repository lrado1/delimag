class Delimag1d():
    """
    Create value aggregation from data with multiselect records.
    
    
    Attributes:
    -----------
    
    
    Methods:
    --------
    
    """
        
    def __init__(self, data, var_group, var_value):
       
        self.data = data
        self.var_group = var_group
        self.var_value = var_value
                
        self.result = []
        self._aggregation_type = 'None'
        self._aggregation_method = 'None'
        
    
    
    
    def __repr__(self):
        
        df_name =[x for x in globals() if globals()[x] is self.data][0]
        
        return (f'DataFrame name: {df_name} \n'
                f'Groupping variable: {self.var_vertical} \n'
                f'Value variable: {self.var_value} \n'
                f'Aggregation type: {self._aggregation_type} \n'
                f'Aggregation method: {self._aggregation_method}')