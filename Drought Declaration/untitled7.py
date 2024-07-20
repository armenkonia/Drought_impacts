# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:06:18 2024

@author: armen
"""

import pandas as pd
import matplotlib.pyplot as plt
storage_indicator = pd.read_csv('not preprocessed/total_storage_percentiles.csv')
storage_indicator['date'] = pd.to_datetime(storage_indicator['date'])
storage_indicator = storage_indicator.loc[(storage_indicator['date'] >= '2017-10-01') & (storage_indicator['date'] <= '2022-09-01')]
storage_indicator['date'] = storage_indicator['date'].dt.strftime('%b %Y')


gw_indicator = pd.read_csv('not preprocessed/state_wells_regional_analysis.csv')
gw_indicator['date'] = pd.to_datetime(gw_indicator['date'])
gw_indicator = gw_indicator.loc[(gw_indicator['date'] >= '2017-10-01') & (gw_indicator['date'] <= '2022-09-01')]
gw_indicator['date'] = gw_indicator['date'].dt.strftime('%b %Y')

#%%
merged_df = pd.merge(storage_indicator[['date','HR_NAME','reservoir_storage']],gw_indicator[['date','HR_NAME','gwchange']], on=['date','HR_NAME'],how='outer')
merged_df['date'] = pd.to_datetime(merged_df['date'])
merged_df['gwchange_interpolate'] = merged_df['gwchange'].interpolate()

#%%

# Define HR names
hr_names = ['Sacramento River', 'San Joaquin River', 'Tulare Lake']

# Create subplots for each HR name
fig, axs = plt.subplots(3, 1, figsize=(1, 15))

# Loop through each HR name and plot data
for i, hr_name in enumerate(hr_names):
    # Extract data for the current HR name
    merged_df_HR = merged_df.loc[merged_df.HR_NAME == hr_name]
    months = merged_df_HR['date']
    reservoir_storage = merged_df_HR['reservoir_storage']
    gwchange = merged_df_HR['gwchange']
    
    # Plot reservoir storage as a bar plot on the current subplot
    axs[i].bar(months, reservoir_storage, label='Reservoir Storage', color='royalblue', width=25)
    
    # Create a secondary y-axis for gwchange
    ax2 = axs[i].twinx()
    ax2.plot(merged_df_HR['date'], merged_df_HR['gwchange'], '-o', color='orange', label='GW Change')
    ax2.plot(merged_df_HR['date'], merged_df_HR['gwchange_interpolate'], '-', linewidth=3, color='orange', label='')
    
    # Label axes and legend
    axs[i].set_ylabel('Reservoir Storage')
    ax2.set_ylabel('GW Change')
    axs[i].set_xlabel('Months')
    axs[i].legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    # Set title
    axs[i].set_title(f'{hr_name}: Reservoir Storage and Groundwater Change per Month')

# Adjust layout
plt.tight_layout()

# Show plots
plt.show()

