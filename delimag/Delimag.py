class Delimag():
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
        
        dist_val = self.distinct_vertical(delim=delim)
        def_dict = defaultdict(int)


        for i in range(len(dist_val)):
            
            q = self.data.loc[self.data[self.var_vertical].str.contains(dist_val[i]).fillna(False),self.var_value]

            if 'count' in calc:
                def_dict[dist_val[i]] = q.shape[0]
                
            elif 'mean' in calc:
                def_dict[dist_val[i]] = q[self.var_value].mean()
                
            elif 'sum' in calc:
                def_dict[dist_val[i]] = q[self.var_value].sum()
                
            elif 'min' in calc:
                def_dict[dist_val[i]] = q[self.var_value].min()
                
            elif 'max' in calc:
                def_dict[dist_val[i]] = q[self.var_value].max() 

        new_df = pd.DataFrame(pd.Series(def_dict))       
        new_df.columns = [calc]
        
        return new_df
    
    
    
    
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

        dist_val = self.distinct_horizontal(delim=delim)
        def_dict = defaultdict(int)


        for i in range(len(dist_val)):
            q = self.data.loc[self.data[self.var_horizontal].str.contains(dist_val[i]).fillna(False),self.var_value]


            if 'count' in calc:
                def_dict[dist_val[i]] = q.shape[0]
                
            elif 'mean' in calc:
                def_dict[dist_val[i]] = q.mean()
            
            elif 'sum' in calc:
                def_dict[dist_val[i]] = q.sum()
            
            elif 'min' in calc:
                def_dict[dist_val[i]] = q.min()
            
            elif 'max' in calc:
                def_dict[dist_val[i]] = q.max()  

        new_df = pd.DataFrame(pd.Series(def_dict))       
        new_df.columns = [calc]
        
        return new_df
        
                
        
        
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
        
        dist_vert = self.distinct_vertical()
        dist_hori = self.distinct_horizontal()
        new_df = pd.DataFrame()
        def_dict = defaultdict(int)
        
        for i in range(len(dist_hori)):
            
            for e in range(len(dist_vert)):
                
                query_data = self.data.loc[
                    (self.data[self.var_horizontal].str.contains(dist_hori[i]).fillna(False)) &
                    (self.data[self.var_vertical].str.contains(dist_vert[e]).fillna(False)) 
                    ]
            
                if calc == 'count':
                    def_dict[dist_vert[e]] = query_data.shape[0]

                elif calc == 'mean':
                    def_dict[dist_vert[e]] = query_data.mean()
                
                elif calc == 'sum':
                    def_dict[dist_vert[e]] = query_data.sum()
                    
                elif calc == 'min':
                    def_dict[dist_vert[e]] = query_data.min()
                    
                elif calc == 'max':
                    def_dict[dist_vert[e]] = query_data.max()
            
            new_df = new_df.append(def_dict, ignore_index=True)
        
        new_df.index = list(dist_hori)
        
        return new_df.fillna(0)


        
        
        
    def result(self, sort_vertical, sort_horizontal, proportionize=False):
        """
        Return the result set of the aggregation in a Pandas DataFrame object in an organized format (sorted, proportionized).
        
        """
        
        
        
        