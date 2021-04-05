class Delimag2d(Delimag1d):
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

    def __init__(self, data, var_group, var_subgroup, var_value):
        
        Delimag1d.__init__(self, data, var_group, var_value)
        
        self.var_subgroup = var_subgroup
    
    
    
    
    def __repr__(self):
        
        return_string = Delimag1d.__repr__(self)
        return_string += (f'Sub-Groupping Variable: {self.var_subgroup}')
        return return_string
   



    def switch_group(self):
        """
        Switch the variables assigned to var_group and var_subgroup.
        
        
        """
        
        temp = self.var_group
        self.var_group = self.var_subgroup
        self.var_subgroup = temp
        
        
        
        
    def distinct_values(self, delim=';', dropna=True, switch_group=True):
        """
        Return a list of distinct values from the col_vertical variable, after splitting the delimited records.
        
        Parameters:
        -----------
        
        delim (String): Specifies the separator to use when splitting the string.
        dropna (Boolean): Remove missing values from the result set.
        
        """
        
        if switch_group == True:
            self.switch_group()
                
        distinct_values = Delimag1d.distinct_values(self, delim=delim, dropna=dropna)
        
        if switch_group == True:
            self.switch_group()

               
        return distinct_values
        
        
        
        
    def aggregate(self, calc=len, delim_vertical=';', delim_horizontal=';'):
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
        
        distinct_vertical = self.distinct_values(delim=delim_vertical, switch_group=False)
        distinct_horizontal = self.distinct_values(delim=delim_horizontal, switch_group=True)
        return_df = pd.DataFrame()
        return_dictionary = defaultdict(int)
        column_names = set()
        
        
        # Filter data.
        
        for i in range(len(distinct_horizontal)):
                
            for e in range(len(distinct_vertical)):
                
                query_data = self.data.loc[
                    (self.data[self.var_subgroup].str.contains(distinct_horizontal[i]).fillna(False)) &
                    (self.data[self.var_group].str.contains(distinct_vertical[e]).fillna(False)) 
                    ]
                
                return_dictionary[distinct_vertical[e]] = calc(query_data[self.var_value])


            # Add aggregation result to return DataFrame.
            
            return_df = return_df.append(return_dictionary, ignore_index=True)
        
        return_df.index = list(distinct_horizontal)
        self.result = return_df.fillna(0)
        
        return self.result


        
        
    def return_result(self, sort_by_vertical='', ascending_vertical=True,
                      sort_by_horizontal='', ascending_horizontal=True, proportionize=''):
        """

        Return the result set of the last aggregation applied on the input DataFrame object in an organized format (sorted, proportionized).
        
        
        Attributes:
        sort_by_vertical (str): Name or list of names of horizontal (axis 1) variables to sort the result table vertically.
        
        ascending_vertical (bool): Sort ascending vs. descending.
        
        sort__by_horizontal (str): Name or list of names of vertical (axis 0) variables to sort the result table horizontall.
        
        ascending_horizontal (bool): Sort ascending vs. descending.
        
        proportionize (Boolean): Recalculate the values of the result DataFrame as proportions.
            - if proportionoze = False: no recalculation will be done.
            - if proportionize = 'column': Values will be shown as the proportion of the column total.
            - if proportionize = 'row': Values will be shown as the proportion of the row total (only possible after .aggregate_cross() method)
            - if proportionize = 'total': Values will be shown as the proportion of the grand total.
        
        """
        
        
#         if sort_by == '':
#             pass
        
#         elif sort_by == 'index':
#             result.sort_index(ascending=ascending, inplace=True)

#         else:
#             result.sort_values(by=sort_by, ascending=ascending, inplace=True)
        
        
        result = self.result.copy()
        
        
        # Apply sort on the data.
        
        if sort_by_vertical == '':
            pass
        
        elif sort_by_vertical == 'index':
            result.sort_index(ascending=ascending_vertical, inplace=True)
        
        else:
            result.sort_values(by=sort_by_vertical, ascending=ascending_vertical, axis=0, inplace=True)
        
        
        
        if sort_by_horizontal == '':
            pass
        
        elif sort_by_horizontal == 'column':
            print('bingo')
            result.sort_index(ascending=ascending_horizontal, inplace=True, axis=1)
            
        else:
            result.sort_values(by=sort_by_horizontal, ascending=ascending_horizontal, axis=1, inplace=True)
            
            
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
        