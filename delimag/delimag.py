class Delimag2d():
    """
    Delimag is a tool to analyze Pandas DataFrame objects with multiselect records.
    
    Makes it possible to create a cross-tabulation after splitting delimited, multiselected records.
        
    Attributes:
    -----------
        data (Pandas DataFrame): A Pandas DataFrame object that we are goint to analyse.
        
        var_vertical (str): The column name of a categorical variable of the data. Will be used as key to group by along the vertical axis of the resulting pivot-talbe.
        
        var_horizontall (str): The column name of a categorical variable of the data. Will be used as key to group by along the horizontal axis of the resulting pivot-talbe.
        
        var_val (str): The column name of the data to aggregate.
        

    Methods:
    --------
        distinct_vertical(delim=';', dropna=True): 
            Return a list of distinct values from the col_vertical variable, after splitting the delimited records.
        
        distinct_horizontaldelim=';', dropna=True):
            Return a list of distinct values from the col_horizontal variable, after splitting the delimited records.
            
        aggregate_vertical(calc='count', delim=';', dropna=True):
            Aggregate the var_val variable with groupping by the var_vertical variable.
            
        aggregate_horizontal(calc='count', delim=';', dropna=True):
            Aggregate the var_val variable with groupping by the var_horizontal variable.            
            
        aggregate_cross(calc='count', delim_vertical=';', delim_horizontal=';'):
            Create a cross tabulation by aggregating the values of the var_val variable by groupping along the var_horizontal and var_vertical variables.
            
        return_result(sort_vertical='', sort_horizontal='', proportionize=''):
            Return an organized (sorted, proportionized) table of the result of the last aggregation applied on the data.
            
            
    """

    def __init__(self, data, var_vertical, var_horizontal="", var_value=""):
        
        self.data = data
        self.result = []
        self.var_vertical = var_vertical
        self.var_horizontal = var_horizontal
        self.var_value = var_value
                
        self._aggregation_type = ''
        self._aggregation_method = ''
    
    
    def __repr__(self):
        
        df_name =[x for x in globals() if globals()[x] is self.data][0]
        
        return (f'DataFrame name: {df_name} \n'
                f'Vertical variable: {self.var_vertical} \n'
                f'Horizontal variable: {self.var_horizontal} \n'
                f'Value variable: {self.var_value} \n'
                f'Aggregation type: {self._aggregation_type} \n'
                f'Aggregation method: {self._aggregation_method}')     
    
    
    
    
    def distinct_vertical(self, delim=';', dropna=True):
        """
        Return a list of distinct values from the col_vertical variable, after splitting the delimited records.
        
        Parameters:
        -----------
        
        delim (String): Specifies the separator to use when splitting the string.
        dropna (Boolean): Remove missing values from the result set.
        
        """
        

        if dropna:
            distinct_values = list({value for values in self.data[self.var_vertical].dropna() 
                                    for value in str(values).split(delim)})
        else:
            distinct_values = list({value for values in self.data[self.var_vertical] 
                                    for value in str(values).split(delim)})
               
        return distinct_values
        
        
        
        
    def distinct_horizontal(self, delim=';', dropna=True):
        """
        Return a list of distinct values from the col_horizontal variable, after splitting the delimited records.
        
        Parameters:
        -----------
        
        delim (String): Specifies the separator to use when splitting the string.
        dropna (Boolean): Remove missing values from the result set.
        
        """
        
        
        if dropna:
            distinct_values = list({value for values in self.data[self.var_horizontal].dropna() 
                                    for value in str(values).split(delim)})
        else:
            distinct_values = list({value for values in self.data[self.var_horizontal] 
                                    for value in str(values).split(delim)})
        
        return distinct_values
       
        
        
    
    def aggregate_vertical(self, calc='count', delim=';'):
        """
        Aggregate the var_val variable with groupping by the var_vertical variable.
        
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
            
            q = self.data.loc[self.data[self.var_vertical].str.contains(distinct_values[i]).fillna(False),self.var_value]

        
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
    
    
    
    
    def aggregate_horizontal(self, calc='count', delim=';'):
        """
        Aggregate the var_val variable with groupping by the var_horizontal variable.
        
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

        distinct_values = self.distinct_horizontal(delim=delim)
        return_dictionary = defaultdict(int)

        
        # Filter data.
        
        for i in range(len(distinct_values)):
            
            q = self.data.loc[self.data[self.var_horizontal].str.contains(distinct_values[i]).fillna(False),self.var_value]

        
        # Apply aggregation on filtered data.
        
            if 'count' in calc:
                return_dictionary[distinct_values[i]] = q.shape[0]
                
            elif 'mean' in calc:
                return_dictionary[distinct_values[i]] = q.mean()
            
            elif 'sum' in calc:
                return_dictionary[distinct_values[i]] = q.sum()
            
            elif 'min' in calc:
                return_dictionary[distinct_values[i]] = q.min()            
            elif 'max' in calc:
                return_dictionary[distinct_values[i]] = q.max()  

                
        # Add aggregation results to return DataFrame.
        
        return_df = pd.DataFrame(pd.Series(return_dictionary))       
        return_df.columns = [calc]
        
        self.result = return_df
        
        return self.result
        
                
        
        
    def aggregate_cross(self, calc='count', delim_vertical=';', delim_horizontal=';'):
        """
        Create a cross-tabulation based on two variables and aggregates a third variables's values based on the cross-groupping.
        
        Parameters:
        -----------
        
        calc (String): Method of aggregation. Possible values:
            - sum
            - mean
            - min
            - max
            - count
        
        delim_vertical (String): Specifies the separator to use when splitting the string in the var_vertical variable.
        
        delim_horizontal (String): Specifies the separator to use when splitting the string in the var_horizontal variable.
        
        dropna (Boolean): Remove missing values from the result set.
        
        """
        
        distinct_vertical = self.distinct_vertical(delim=delim_vertical)
        distinct_horizontal = self.distinct_horizontal(delim=delim_horizontal)
        return_df = pd.DataFrame()
        return_dictionary = defaultdict(int)
        
        
        # Filter data.
        
        for i in range(len(distinct_horizontal)):
            
            for e in range(len(distinct_vertical)):
                
                query_data = self.data.loc[
                    (self.data[self.var_horizontal].str.contains(distinct_horizontal[i]).fillna(False)) &
                    (self.data[self.var_vertical].str.contains(distinct_vertical[e]).fillna(False)) 
                    ]
       
    
        # Apply aggregation on filtered data.
        
                if calc == 'count':
                    return_dictionary[distinct_vertical[e]] = query_data.shape[0]

                elif calc == 'mean':
                    return_dictionary[distinct_vertical[e]] = query_data[self.var_value].mean()
                
                elif calc == 'sum':
                    return_dictionary[distinct_vertical[e]] = query_data[self.var_value].sum()
                    
                elif calc == 'min':
                    return_dictionary[distinct_vertical[e]] = query_data[self.var_value].min()
                    
                elif calc == 'max':
                    return_dictionary[distinct_vertical[e]] = query_data[self.var_value].max()
            
            
            # Add aggregation result to return DataFrame.
            
            return_df = return_df.append(return_dictionary, ignore_index=True)
        
        return_df.index = list(distinct_horizontal)
        self.result = return_df.fillna(0)
        
        return self.result


        
        
        def return_result(self, sort_vertical='', sort_horizontal='', proportionize=''):
        """

        Return the result set of the last aggregation applied on the input DataFrame object in an organized format (sorted, proportionized).
        
        
        Attributes:
        sort_vertical (String): Name or list of names of horizontal (axis 1) variables to sort the result table vertically.
        
        sort_horizontal (String): Name or list of names of vertical (axis 0) variables to sort the result table horizontall.
        
        proportionize (Boolean): Recalculate the values of the result DataFrame as proportions.
            - if proportionoze = False: no recalculation will be done.
            - if proportionize = 'column': Values will be shown as the proportion of the column total.
            - if proportionize = 'row': Values will be shown as the proportion of the row total (only possible after .aggregate_cross() method)
            - if proportionize = 'total': Values will be shown as the proportion of the grand total.
        
        """
        
        result = self.result.copy()
        
        
        # Apply sort on the data.
        
        if sort_vertical != '':
            result.sort_values(by=sort_vertical, axis=0, inplace=True)
        
        if sort_horizontal != '':
            result.sort_values(by=sort_horizontal, axis=1, inplace=True)
            
            
        # Re-calculate values into proportions.
        
        if proportionize in ('column', 'row', 'total', ''):
        
            if proportionize == 'column':

                for col in result.columns:
                    total = result[col].sum()

                    for row in result.index:
                        result.loc[row, col] = result.loc[row, col] / total

            elif proportionize == 'row':

                for row in result.index:
                    total = result.loc[row,].sum()

                    for col in result.columns:
                        result.loc[row, col] = result.loc[row, col] / total

            elif proportionize == 'total':

                total = sum([result[x].sum() for x in result.columns])
                for col in result.columns:
                    for row in result.index:
                        result.loc[row, col] = result.loc[row, col] / total
        
        else:
            raise ValueError("proportionize parameter can only accept the following values:"\
                             "'column', 'row', 'total' or can be left empty.")
                
        
        return result
        