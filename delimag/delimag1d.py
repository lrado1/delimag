class Delimag1d():
    """
    Create value aggregation from data with multiselect records.
    
    
    Attributes:
    -----------
    data (Pandas DataFrame): A Pandas DataFrame object that we are goint to analyse.
    
    var_group(str): Variable (column) name to group by on the result table index.
    
    var_value(str): Variable (column) name to aggregate.
    
    
    Methods:
    --------
    
    distinct_values(delim=';', dropna=True): 
        - Return a list of distinct values from the groupping variable, after splitting the delimited records.
    
    aggregate_values(calc='count', delim=';'):
        - Aggregate the values of the value variable with groupping by the groupping variable.
    
    return_result(sort_by='', ascending=True, proportionize=False):
        - Return the result set of the last aggregation applied on the input DataFrame object, in an organized format (sorted, proportionized).
    
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
        
        delim (str): Specifies the separator to use when splitting the string.
        dropna (bool): Remove missing values from the result set.
        
        """
        

        if dropna = True:
            distinct_values = list({value for values in self.data[self.var_group].dropna() 
                                    for value in str(values).split(delim)})
        elif dropna = False:
            distinct_values = list({value for values in self.data[self.var_group] 
                                    for value in str(values).split(delim)})
        
        else:
            raise ValueError("Dropna parameter can only accept Boolean values.")
               
        return distinct_values
    
    
    
    
        def aggregate_values(self, calc='count', delim=';'):
        """
        Aggregate the values of the value variable with groupping by the groupping variable.
        
        Parameters:
        -----------
     
        calc (str or list of str): Method name or list of method names of aggregation type.
            Example:
                - np.sum, np.mean, lambda functions etc...
                - d1 = Delimag1d(data, 'Category', 'Value')
                  d1.aggregate_values(lambda x: np.mean(x <= 20))
                
        delim (str): Specifies the separator to use when splitting the string.
        
        dropna (bool): Remove missing values from the result set.
        
        """

        
        return_dictionary = defaultdict(int)
        distinct_values = self.distinct_values(delim=delim, dropna=dropna)
        column_names = set()
        
        
        # Filter data.
        
        for i in range(len(distinct_values)):
            
            q = self.data.loc[self.data[self.var_group].str.contains(distinct_values[i]).fillna(True),self.var_value]

            
        # Apply aggregation on filtered data.
        
            if hasattr(calc, '__iter__'):
                for c in calc:
                    return_dictionary.setdefault(distinct_values[i], []).append(c(q))
                    column_names.add(c.__name__)
            else:
                return_dictionary.setdefault(distinct_values[i], []).append(calc(q))
                column_names.add(calc.__name__)

                
        # Add aggregation results to return DataFrame
        
        return_df = pd.DataFrame.from_dict(return_dictionary).transpose()
        return_df.columns = list(column_names)
        
        self.result = return_df
        
        return self.result
    
    
    
    
    def return_result(self, sort_by='', ascending=True, proportionize=False):
        """

        Return the result set of the last aggregation applied on the input DataFrame object, in an organized format (sorted, proportionized).
        
        
        Attributes:
        sort_by (str): Column name or list of column names to sort the result table. Pass 'index' to sort by the index label.
        
        ascending (bool): Sort ascending vs. descending. Specify list for multiple sort orders. If this is a list of bools, must match the length of the by.
                
        proportionize (bool): Recalculate the values of the result DataFrame as proportions.
        
        """
        
        
        result = self.result.copy()
        
        
        # Apply sort on the data.
        
        if sort_by == '':
            pass
        
        elif sort_by == 'index':
            result.sort_index(ascending=ascending, inplace=True)

        else:
            result.sort_values(by=sort_by, ascending=ascending, inplace=True)
        
            
        # Re-calculate values into proportions.
        
        if proportionize == True:
            total = result.sum()
            for row in result.index:

                result.loc[row,:] = result.loc[row,:] / total

        elif proportionize == False:
            pass
        
        else:
            raise ValueError("proportionize parameter should be boolean (True/False).")
                
        
        return result
    