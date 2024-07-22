# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:17:46 2024

@author: armen
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import plotly.express as px
import seaborn as sns

os.chdir(r"C:\Users\armen\OneDrive - UCLA IT Services\UCLA Projects\COEQWAL")
#%%
# import land areas for ag, ub, fl and nl for all Tulare, San Joaquin, and Sacramento
metadata = pd.read_pickle(r'Data\Pickle\land_area_HR.pk')
# for i, data in enumerate(metadata):
#     # Update the DataFrame in place based on the condition
#     metadata[i] = data[data.index.isin(['Tulare Lake', 'San Joaquin River', 'Sacramento River'])]
    
land_area_all, land_area_ag, land_area_ub, land_area_fl, land_area_nl = metadata


# restructuring dataframes for plotting purposes
def restructure_df_for_plot (total_area_all):
    total_area_plot = total_area_all.iloc[:,:-2]
    total_area_plot.columns = ['Field_2016','Field_2018','Field_2020','Field_2021','Field_2022']
    total_area_plot = total_area_plot.transpose()
    return total_area_plot

land_area_all = restructure_df_for_plot (land_area_all)
land_area_ag = restructure_df_for_plot (land_area_ag)
land_area_ub = restructure_df_for_plot (land_area_ub)
land_area_fl = restructure_df_for_plot (land_area_fl)
land_area_nl = restructure_df_for_plot (land_area_nl)
#%%
# Creating MultiIndexes for each DataFrame
land_area_ag.columns = pd.MultiIndex.from_product([['Agriculture'], land_area_ag.columns])
land_area_ub.columns = pd.MultiIndex.from_product([['Urban'], land_area_ub.columns])
land_area_fl.columns = pd.MultiIndex.from_product([['Fallow'], land_area_fl.columns])

# Concatenate all three DataFrames at once
meta_df = pd.concat([land_area_ag, land_area_ub, land_area_fl], axis=1)
meta_df.columns = meta_df.columns.rename(['Land Type', 'Region'], level=[0, 1])
meta_df.index = ['2016','2018','2020','2021','2022']
#%%
base_year_data = meta_df.loc['2018']
percentage_change_from_2018 = meta_df.sub(base_year_data, axis='columns').divide(base_year_data, axis='columns')*100
percentage_change_from_2018 = percentage_change_from_2018.drop('2018')

#%%
landiq_2016_crops,landiq_2018_crops,landiq_2020_crops,landiq_2021_crops,landiq_2022_crops, all_hr_crops=pd.read_pickle(r'Data\Pickle\crop_area_HR.pk')
meta_df_crops = pd.concat(all_hr_crops, axis=1)
meta_df_crops.columns = meta_df_crops.columns.rename(['Year', 'Region'], level=[0, 1])
melted_df = pd.melt(meta_df_crops,ignore_index=False)
meta_df_crops = melted_df.reset_index(names='Crop Type')
meta_df_crops_pivot = meta_df_crops.pivot_table(index='Year', columns=['Region', 'Crop Type'], values='value',dropna=False)

#%%
# Pivot the data: rows are 'Year', columns are 'Region', values are 'value'
regional_sum = meta_df_crops.groupby(['Region','Year'])['value'].sum()
regional_sum = regional_sum.reset_index()
regional_sum_pivot = regional_sum.pivot_table(index='Year', columns=['Region'], values='value',dropna=False) 
#%%
# Pivot the data: rows are 'Year', columns are 'Crop Type', values are 'value'
meta_df_crops_selected = meta_df_crops.loc[meta_df_crops['Region'].isin(['Tulare Lake', 'San Joaquin River', 'Sacramento River'])]
regional_sum = meta_df_crops.groupby(['Crop Type','Year'])['value'].sum()
regional_sum = regional_sum.reset_index()
regional_sum_pivot = regional_sum.pivot_table(index='Year', columns=['Crop Type'], values='value',dropna=False) 

#%%

base_year_data = regional_sum_pivot.loc['2018']
percentage_change_from_2018 = regional_sum_pivot.sub(base_year_data, axis='columns').divide(base_year_data, axis='columns')*100      
df = percentage_change_from_2018.T
#%%
# Calculate YoY growth
growth_df = regional_sum_pivot.pct_change().dropna() * 100

#%%
growth_df = regional_sum_pivot.diff(axis=0)
#%%
import pandas as pd

# Define the crop types and their descriptions
data = [
    ('C', "Citrus and subtropical (' C')"),
    ('D', "Deciduous fruits and nuts (' D')"),
    ('E', "Entry denied"),
    ('F', "Field crops (' F')"),
    ('G', "Grain and hay crops (' G')"),
    ('I', "Idle (' I')"),
    ('NB', "Barren and wasteland ('NB')"),
    ('NC', "Native classes, unsegregated ('NC')"),
    ('NR', "Native riparian vegetation ('NR')"),
    ('NS', "Not surveyed ('NS')"),
    ('NV', "Native vegetation ('NV')"),
    ('NW', "Water surface ('NW')"),
    ('P', "Pasture (' P')"),
    ('R', "Rice (' R')"),
    ('S', "Semi-agricultural and incidental to agriculture ('S ')"),
    ('T', "Truck, nursery, and berry crops (' T')"),
    ('U', "Urban-residential, commercial, and industrial, unsegregated ('U ')"),
    ('UC', "Urban commercial ('UC')"),
    ('UI', "Urban industrial ('UI')"),
    ('UR', "Urban residential single and multi family units, includes trailer parks ('UR')"),
    ('UV', "Urban vacant ('UV')"),
    ('V', "Vineyards (' V')"),
    ('X', "Unclassified fallow"),
    ('YP', "Young Perennial"),
    ('Z', "Outside of the study area ('Z ')")
]

# Create a DataFrame
crop_types_df = pd.DataFrame(data, columns=['Code', 'Description'])
crop_types_df['Description'] = crop_types_df['Description'].str.replace(r" \(.*?\)", "", regex=True)
meta_df_crops = pd.merge(meta_df_crops, crop_types_df, left_on='Crop Type', right_on='Code', how='left')
meta_df_crops.drop('Code', axis=1, inplace=True)


#%%
meta_df_crops['New Crop Type'] = meta_df_crops['Crop Type'].apply(lambda x: 'Young Perennial' if x == 'YP' else 'Crops')
#%%
meta_df_crops_3_reg = meta_df_crops.loc[meta_df_crops.Region.isin(['Tulare Lake', 'Sacramento River','San Joaquin River'])]
meta_df_crops_pivot = meta_df_crops_3_reg.pivot_table(index='Year', columns=['Region', 'New Crop Type'], values='value', aggfunc='sum',dropna=False)

#%%
meta_df_crops_pivot = meta_df_crops_3_reg.pivot_table(index='Year', columns=['Region', 'Crop Type'], values='value', aggfunc='sum',dropna=False)

