class Delimag():
    """
    Delimag is a tool to analyze Pandas DataFrame objects with multiselect records.
        
        
    Attributes:


    Methods:

            
    """

    def __init__(self, data, var_vertical, var_horizontal="", var_value=""):
        
        self.data = data
        self.result = self.data
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
        
        self.result = new_df
        
        return self.result
    
    
    
    
    def aggregate_horizontal(self, calc='count', delim=';', drop_na=True):
        """
        Aggregate along the col_horizontal variable.
        
        """

        dist_val = self.distinct_horizontal(delim=delim, drop_na=drop_na)
        def_dict = defaultdict(int)


        for i in range(len(dist_val)):
            q = self.data.loc[self.data[self.var_horizontal].str.contains(dist_val[i]).fillna(False),self.var_value]


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
        
        self.result = new_df
        
        return self.result
        
                
        
        
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
                    
                elif calc == 'max':
                    def_dict[dist_vert[e]] = query_data[self.var_value].max()
            
            new_df = new_df.append(def_dict, ignore_index=True)
        
        new_df.index = list(dist_hori)
        
        self.result = new_df.fillna(0)
        
        return self.result


        
        
        
        def return_result(self, sort_vertical='', sort_horizontal='', proportionize=False):
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
        
        if sort_vertical != '':
            result.sort_values(by=sort_vertical, axis=0, inplace=True)
        
        if sort_horizontal != '':
            result.sort_values(by=sort_horizontal, axis=1, inplace=True)

        
        
        if proportionize in ('column', 'row', 'total', ''):
        
            if proportionize == 'column':

                for col in result.columns:
                    total = result[col].sum(axis=0)

                    for row in result.index:
                        result.loc[row, col] = result.loc[row, col] / total

            elif proportionize == 'row':

                for row in result.index:
                    total = result.loc[index,].sum(axis=1)

                    for row in result.index:
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
        