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