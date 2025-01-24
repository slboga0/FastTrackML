import os
import numpy as np
import pandas as pd


def convert_cards_to_df(cards, max_npp, max_nwrk):
    # Convert list of dictionaries to dataframe
    features = pd.DataFrame(cards)

    # Identify dataframe columns that are lists
    list_cols = []
    for col_name in features.columns:
        if isinstance(features[col_name][0], list):
            list_cols.append(col_name)

    # Identify pp versus wrk column of lists
    pp_col_names = []
    wrk_col_names = []
    for col_name in list_cols:
        pcs = col_name.split('_')
        if pcs[0] == 'pp':
            pp_col_names.append(col_name)
        else:
            wrk_col_names.append(col_name)

    # Split WRK dataframe list elements into columns
    features = split_df_into_columns(features, max_nwrk, wrk_col_names)

    # Split PP dataframe list elements into columns
    features = split_df_into_columns(features, max_npp, pp_col_names)

    return features


#def split_df_into_columns(features, max_nwrk, wrk_col_names):
#    for col_name in wrk_col_names:
#        new_col_names = []
#        for i in range(0, max_nwrk):
#            new_col_names.append(col_name + '_' + str(i))
#        new_columns_df = pd.DataFrame(features[col_name].tolist()).T  # Create new columns in a single DataFrame
#        new_columns_df = pd.DataFrame(features['col_name'].tolist(), columns=features['col_name'].tolist())
#
#        features = pd.concat([features, new_columns_df], axis=1)  # Efficiently concatenate
#        features.drop(col_name, axis=1, inplace=True)  # Drop the original column in-place
#
#    return features

def split_df_into_columns(features, max_nwrk, wrk_col_names):
    for col_name in wrk_col_names:
        new_col_names = [col_name + '_' + str(i) for i in range(max_nwrk)]  # Generate new column names
        new_columns_df = pd.DataFrame(features[col_name].tolist(), columns=new_col_names)  # Create new columns with correct names
        features = pd.concat([features, new_columns_df], axis=1)  # Concatenate new columns to the original DataFrame
        features.drop(col_name, axis=1, inplace=True)  # Drop the original column in-place

    return features
