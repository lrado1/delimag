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
                f'Groupping variable: {self.var_group} \n'
                f'Value variable: {self.var_value} \n'
                f'Aggregation type: {self._aggregation_type} \n'
                f'Aggregation method: {self._aggregation_method}')
    
    
    
    
    def distinct_values(self, delim=';', dropna=True):
        """
        Return a list of distinct values from the groupping variable, after splitting the delimited records.
        
        Parameters:
        -----------
        
        delim (String): Specifies the separator to use when splitting the string.
        dropna (Boolean): Remove missing values from the result set.
        
        """
        

        if dropna:
            distinct_values = list({value for values in self.data[self.var_group].dropna() 
                                    for value in str(values).split(delim)})
        else:
            distinct_values = list({value for values in self.data[self.var_group] 
                                    for value in str(values).split(delim)})
               
        return distinct_values
    
    
    
    
        def aggregate_values(self, calc='count', delim=';'):
        """
        Aggregate the values of the value variable with groupping by the groupping variable.
        
        Parameters:
        -----------
        
        calc (String): Method of aggregation. Possible values:
            - sum
            - mean
            - min
            - max
            - count
        
        delim (String): Specifies the separator to use when splitting the string.
        
        dropna (Boolean): Remove missing values from the result set.
        
        """
        
        return_dictionary = defaultdict(int)
        distinct_values = self.distinct_vertical(delim=delim)
        
        
        # Filter data.
        
        for i in range(len(distinct_values)):
            
            q = self.data.loc[self.data[self.var_group].str.contains(distinct_values[i]).fillna(False),self.var_value]

        
        # Apply aggregation on filtered data.
        
            if 'count' in calc:
                return_dictionary[distinct_values[i]] = q.shape[0]
                
            elif 'mean' in calc:
                return_dictionary[distinct_values[i]] = q[self.var_value].mean()
                
            elif 'sum' in calc:
                return_dictionary[distinct_values[i]] = q[self.var_value].sum()
                
            elif 'min' in calc:
                return_dictionary[distinct_values[i]] = q[self.var_value].min()
                
            elif 'max' in calc:
                return_dictionary[distinct_values[i]] = q[self.var_value].max() 

        
        # Add aggregation results to return DataFrame
        
        return_df = pd.DataFrame(pd.Series(return_dictionary))       
        return_df.columns = [calc]
        
        self.result = return_df
        
        return self.result
    
    
    