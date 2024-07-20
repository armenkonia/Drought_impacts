# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 16:01:18 2024

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
# import land areas for ag, ub, fl and nl for all HR regions
land_area_all, land_area_ag, land_area_ub, land_area_fl, land_area_nl = pd.read_pickle(r'Data\Pickle\land_area_HR.pk')

#%%
# # import land areas for ag, ub, fl and nl for all Tulare, San Joaquin, and Sacramento
# metadata = pd.read_pickle(r'Data\Pickle\land_area_HR.pk')
# for i, data in enumerate(metadata):
#     # Update the DataFrame in place based on the condition
#     metadata[i] = data[data.index.isin(['Tulare Lake', 'San Joaquin River', 'Sacramento River'])]
    
# land_area_all, land_area_ag, land_area_ub, land_area_fl, land_area_nl = metadata
#%%
# restructuring dataframes for plotting purposes
def restructure_df_for_plot (total_area_all):
    total_area_plot = total_area_all.iloc[:,:-2]
    total_area_plot.columns = ['Field_2016','Field_2018','Field_2020','Field_2021','Field_2022']
    total_area_plot = total_area_plot.transpose()
    return total_area_plot

land_area_all_plot = restructure_df_for_plot (land_area_all)
land_area_ag_plot = restructure_df_for_plot (land_area_ag)
land_area_ub_plot = restructure_df_for_plot (land_area_ub)
land_area_fl_plot = restructure_df_for_plot (land_area_fl)
land_area_nl_plot = restructure_df_for_plot (land_area_nl)

#%%

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 10), sharey=True)

land_area_ag_plot.plot(legend=True, ax=ax1)
ax1.set_title('Agriculture')
ax1.tick_params(axis='x', labelsize=8, rotation=45)

land_area_ub_plot.plot(legend=False, ax=ax2)
ax2.set_title('Urban')
ax2.tick_params(axis='x', labelsize=8, rotation=45)

land_area_fl_plot.plot(legend=False, ax=ax3)
ax3.set_title('Fallow')
ax3.tick_params(axis='x', labelsize=8, rotation=45)

# Add labels outside the figure
figtext_params = dict(x=0.5, y=-0.05, horizontalalignment='center', verticalalignment='center', fontsize=14)
plt.figtext(**figtext_params, s='X-axis Label')
plt.figtext(**figtext_params, s='Y-axis Label', rotation='vertical')

fig.suptitle('Temporal Evolution of Land Types for Top Agricultural Regions in California')
plt.show()

#this is from field classification 3
#%%

all_land_area = pd.concat([land_area_all.loc['Total'], land_area_ag.loc['Total'], land_area_ub.loc['Total'], land_area_fl.loc['Total'], land_area_nl.loc['Total']], axis=1)
all_land_area = all_land_area.iloc[:5,:]
all_land_area.columns = ['all','ag','ub','fl','nl']
all_land_area['total']= all_land_area['ag'] + all_land_area['ub'] + all_land_area['fl'] + all_land_area['nl']
all_land_area['ag+fl']= all_land_area['ag'] + all_land_area['fl']

#%%
all_land_area = all_land_area.loc[:,['total','ag','ub','fl','nl','ag+fl']]
# Plotting each column
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 8))

for i, (column, ax) in enumerate(zip(all_land_area.columns, axes.flatten())):
    all_land_area[column].plot(ax=ax, marker='o', linestyle='-', color='b')
    ax.set_title(column)
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')

plt.tight_layout()
plt.show()

# %%
landiq_2016_crops,landiq_2018_crops,landiq_2020_crops,landiq_2021_crops,landiq_2022_crops, all_hr_crops= pd.read_pickle(r'Data\Pickle\crop_area_HR.pk')

#%%
# only 3 main hr regions
metadata = pd.read_pickle(r'Data\Pickle\crop_area_HR.pk')
metadata = metadata[:5] 
for i, data in enumerate(metadata):
    metadata[i] = data.loc[:,['Tulare Lake', 'San Joaquin River', 'Sacramento River']]
    
landiq_2016_crops,landiq_2018_crops,landiq_2020_crops,landiq_2021_crops,landiq_2022_crops=  metadata
#%%

# Classification based on hydrological region
df = pd.concat([landiq_2016_crops.sum(), landiq_2018_crops.sum(),landiq_2020_crops.sum(), landiq_2021_crops.sum(),landiq_2022_crops.sum()],axis=1) 
df.columns = ['2016', '2018', '2020', '2021','2022']
df = df.sort_index()
fig = px.bar(df, x=df.index, y=df.columns, title="Temporal Changes in Crop Distribution Across Hydrological Regions", labels={'index': 'Hydrological Region', 'value': 'Crop Quantitiy'}, height=600,barmode='group')
# Save the figure to an HTML file
fig.write_html("Results/Trial/Temporal Changes in Crop Distribution Across Hydrological Regions.html")

#%%

# Classification based on crop type
df = pd.concat([landiq_2016_crops.sum(axis=1), landiq_2018_crops.sum(axis=1),landiq_2020_crops.sum(axis=1), landiq_2021_crops.sum(axis=1), landiq_2022_crops.sum(axis=1)],axis=1) 
df.columns = ['2016', '2018', '2020', '2021', '2022']
fig = px.bar(df, x=df.index, y=df.columns, title="Temporal Changes in 3 AG Regions Crop Distribution", labels={'index': 'Crop Type', 'value': 'Crop Quantity'}, height=600,barmode='group')
# Save the figure to an HTML file
fig.write_html("Results/Trial/Temporal Changes in California Crop Distribution.html")

#%%

all_hr_crops = all_hr_crops[0:10] #THERE IS ONE DATAFRAME THAT IS MISSING, SO WE CROSS THAT OUT
# Create subplots with 2 rows for each dataframe
fig, axes = plt.subplots(len(all_hr_crops)//2, 2, figsize=(12, 8), sharey=True)
axes = axes.flatten()

for i, df in enumerate(all_hr_crops):
    # Copy dataframe and extract the first level of the multi-index
    df = df.copy()
    df.columns = df.columns.get_level_values(0)
    
    # Title of Dataframe
    df_title = all_hr_crops[i].columns[0][1]
    
    # Reshape the DataFrame using melt
    df_melted = df.reset_index().melt(id_vars='index', var_name='Year', value_name='Value')

    # Create a barplot in the current subplot
    sns.barplot(data=df_melted, x='index', y='Value', hue='Year', ax=axes[i])

    # Set subplot title
    axes[i].set_title(df_title)
    
    # Remove Legend
    axes[i].legend_.remove()


# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()

#%%
all_hr_crops = [all_hr_crops[i] for i in [0, 1, 3]]

fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharey=True)
axes = axes.flatten()

for i, df in enumerate(all_hr_crops):
    # Copy dataframe and extract the first level of the multi-index
    df = df.copy()
    df.columns = df.columns.get_level_values(0)
    
    # Title of Dataframe
    df_title = all_hr_crops[i].columns[0][1]
    
    # Reshape the DataFrame using melt
    df_melted = df.reset_index().melt(id_vars='index', var_name='Year', value_name='Value')

    # Create a barplot in the current subplot
    sns.barplot(data=df_melted, x='index', y='Value', hue='Year', ax=axes[i])

    # Set subplot title
    axes[i].set_title(df_title)
    
    # Remove Legend
    axes[i].legend_.remove()


# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()