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
        
        if drop_na:
            distinct_values = list({value for values in self.data[self.var_vertical].dropna() 
                                    for value in str(values).split(delim)})
        else:
            distinct_values = list({value for values in self.data[self.var_vertical] 
                                    for value in str(values).split(delim)})
        
        return distinct_values
        
        
        
        
    def distinct_horizontal(self, delim=';', drop_na=True):
        """
        Return a list of distinct values from the col_horizontal variable, after splitting the delimited records.
        
        """
        
        if drop_na:
            distinct_values = list({value for values in self.data[self.var_horizontal].dropna() 
                                    for value in str(values).split(delim)})
        else:
            distinct_values = list({value for values in self.data[self.var_horizontal] 
                                    for value in str(values).split(delim)})
        
        return distinct_values
       
        
        
    
    def aggregate_vertical(self, calc='count', delim=';', drop_na=True):
        """
        Aggregate along the col_vertical variable.
        
        """
        
        dist_val = self.distinct_vertical(delim=delim, drop_na=drop_na)
        def_dict = defaultdict(int)


        for i in range(len(dist_val)):
            
            q = self.data.loc[self.data[self.var_vertical].str.contains(dist_val[i]).fillna(False),self.var_value]

            # Appling the calculation on each sub-subset DataFrame
            if 'mean' in calc:
                pass
                def_dict[dist_val[i]] = q.mean()
            elif 'count' in calc:
                def_dict[dist_val[i]] = q.shape[0]
            elif 'sum' in calc:
                pass
                def_dict[dist_val[i]] = q.sum()   

        new_df = pd.DataFrame(pd.Series(def_dict))       
        new_df.columns = [calc]
        
        return new_df
    
    
    
    
    def aggregate_horizontal(self, calc='count', delim=';', drop_na=True):
        """
        Aggregate along the col_horizontal variable.
        
        """

        dist_val = self.distinct_horizontal(delim=delim, drop_na=drop_na)
        def_dict = defaultdict(int)


        for i in range(len(dist_val)):
            q = self.data.loc[self.data[self.var_horizontal].str.contains(dist_val[i]).fillna(False),self.var_value]

            # Appling the calculation on each sub-subset DataFrame
            if 'mean' in calc:
                pass
                #def_dict[ddv[i]] = q.mean()
            elif 'count' in calc:
                def_dict[dist_val[i]] = q.shape[0]
            elif 'sum' in calc:
                pass
                #def_dict[ddv[i]] = q.sum()   

        new_df = pd.DataFrame(pd.Series(def_dict))       
        new_df.columns = [calc]
        
        return new_df
        
                
        
        
    def aggregate_cross(self, calc='count', delim_vertical=';', delim_horizontal=';'):
        """
        Create a cross-tabulation based on two variables and aggregates a third variables's values based on the cross-groupping.
        
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
                    def_dict[dist_vert[e]] = query_data[self.var_value].mean()
                
                elif calc == 'sum':
                    def_dict[dist_vert[e]] = query_data[self.var_value].sum()
                    
                elif calc == 'min':
                    def_dict[dist_vert[e]] = query_data[self.var_value].min()
            
            new_df = new_df.append(def_dict, ignore_index=True)
        
        new_df.index = list(dist_hori)
        
        return new_df.fillna(0)
        
        
        
        
    def condition(self, vertical, horizontal, value):
        """
        Filter the result set of the aggregation. 
        
        """

        
        
        
    def result(self, sort_vertical, sort_horizontal, proportionize=False):
        """
        Return the result set of the aggregation in a Pandas DataFrame object in an organized format (sorted, proportionized).
        
        """
        
        
        
        