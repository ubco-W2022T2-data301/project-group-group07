# imports

import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt

def processed_df(): 
    """
    This function loads a dataset with salary integrated to usd. 

    Returns:
        df: Dataframe
            Processed dataframe. 
    """
    df = pd.read_csv('../data/processed/ds_salaries_1.csv')
    df = (
        df.drop(columns={'salary', 'salary_currency'})
        .rename(columns = {'salary_in_usd':'salary'})
    )
    return df


def boxplot(data=None, x=None, y=None, hue=None, order=None, hue_order=None,
            title=None, xlabel=None, ylabel=None, figsize=None):
    """
    This function is a conbination of sns.boxplot(), sns.set(), and plt.figure . 
    
    Args:
        data: Dataframe, default:None 
            Dataframe used to display a boxplot. 
        x: String, default:None
            Column name in data to be considered as x-axis. 
        y: String, default:None
            Column name in data to be considered as y-axis. 
        hue: String, optional, default:None
            Column name in data to be considered as hue. 
        order: list of Strings, optional, default:None
            Order to plot the categorical levels in. 
        hue_order: list of Strings, optional, default:None
            Hue order to plot the categorical levels within each category. 
        title: String, optional, default:None
            Title of the plot. 
        xlabel: String, optional, default:None
            X-label of the plot. 
        ylabel: String, optional, default:None
            Y-label of the plot. 
        figsize: (float, float), optional, default:None 
            Figure size of the plot. 

    Returns:
        plot: Boxplot
            Boxplot designed by specified 
    """
    plt.figure(figsize=figsize)
    plt.clf()
    plot = (
        sns.boxplot(data = data, x = x, y = y, hue=hue, order=order, hue_order=hue_order)
        .set(title = title, xlabel = xlabel, ylabel = ylabel)       
    )
    plt.figure(figsize=(6.4, 4.8)) # restore default value
    return plot


def count_category(data=None, column=None, ascending = False):
    """
    This function counts the number of rows of each unique element within the specified column. 
    
    Args:
        data: Dataframe, default:None
            Dataframe to be consedered in counting. 
        column: String, default:None
            Column that is grouped by and counted unique elements. 
        ascending: boolean, optional, default:False
            Specifies whether the elements are sorted in ascending or descending order 
            based on the count. 
            By default, descending order.

    Returns:
        df: Dataframe
            Dataframe for each item in specified group and the number of corresponding elements. 
    """
    df = (
        data.groupby(column)
            .count()
            .rename(columns = {data.columns[0]:'count'})
            .sort_values('count',ascending = ascending)
            .iloc[:,:1]
            .reset_index()
    )
    return df


def extract_match(data=None, col=None, lst=None):
    """
    This function extracts the rows that matches any of the elements in lst within specified column. 

    Args:
        data: Dataframe, default:None
            Dataframe to be extracted from. 
        col: String, default:None
            Name of the column to be considered in finding matches
        lst: list of Strings, default:None
            List of elements to be matched with. 
            Rows that match with any elements in this list will be included in the output. 
    Returns:
        df: Dataframe
            Dataframe that only holds the matched columns. 
    """
    
    df = (
        data[data[col].isin(lst)].reset_index(drop = True)
    )
    return df


def count_category_groupby(data=None, column1=None, column2=None, 
                           order_column1=None, order_column2=None):
    """
    This function counts the number of elements of unique elements of column2 within the unique elements in column1. 

    Args:
        data: Dataframe, default:None
            Dataframe to be considered. 
        column1: String, default:None
            Column name to be grouped by on rows. 
        column2: String, default:None
            Column name to be grouped by on columns.
        order_column1: list of String, optional, default:None
            List of unique elements in column1.  
            Rows are ordered as specified. 
        order_column2: list of String, optional, default:None
            List of unique elements in column2.  
            Columns are ordered as specified. 

    Returns:
        merged_df: Dataframe
            Dataframe of number of elements of unique elements in column1 versus unique elements in column2. 
            The rows and columns are ordered as specified. 
    """
    list_df = list()
    for i in data[column2].unique():
        df = count_category(data = data[data[column2] == i], column = column1).rename(columns={'count':i})
        list_df.append(df)
        
    merged_df = list_df[0]
    for i in list_df[1:]:
        merged_df = pd.merge(merged_df, i, how='outer')
    
    
    merged_df = (
        merged_df.set_index(keys=column1)
                 .reindex(index=order_column1)
                 .reindex(columns=order_column2)
                 .reset_index()
    )
    return merged_df


