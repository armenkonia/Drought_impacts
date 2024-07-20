# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 20:28:59 2024

@author: armen
"""
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import ipywidgets as widgets
from ipywidgets import interactive
from IPython.display import display
import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr


filepath = '../Outputs/cum_pr_WY.nc'
ds = xr.open_dataset(filepath)
df = ds.to_dataframe()
df.drop(columns='crs',inplace=True)
df.reset_index(inplace=True)
df = df.pivot(index=['lon', 'lat'], columns='WaterYear', values='Precipitation')

#%%
# get average pr for each cell 
df_91_20 = df.loc[:,'1991':'2020']
df_mean = df_91_20.mean(axis=1).to_frame(name='Mean Precipitation')

#%%
df_20 = df[['2020']]
df_20['mean'] = df_mean['Mean Precipitation']
df_20['cum_loss'] = df_20['2020']/df_20['mean']*100

df_20_21 = df.loc[:,['2020','2021']]
df_20_21['sum'] = df_20_21.sum(axis=1)
df_20_21['mean'] = df_mean['Mean Precipitation']
df_20_21['2x mean'] = df_20_21['mean']*2
df_20_21['cum_loss'] = df_20_21['sum']/df_20_21['2x mean']*100

df_20_21_22 = df.loc[:,['2020','2021','2022']]
df_20_21_22['sum'] = df_20_21_22.sum(axis=1)
df_20_21_22['mean'] = df_mean['Mean Precipitation']
df_20_21_22['3x mean'] = df_20_21_22['mean']*3
df_20_21_22['cum_loss'] = df_20_21_22['sum']/df_20_21_22['3x mean']*100
#%%
df_merged = pd.merge(df_20, df_20_21, on=['lat', 'lon'], suffixes=('_20', '_20_21'))
df_merged = pd.merge(df_merged, df_20_21_22.add_suffix('_20_21_22'), on=['lat', 'lon'])
# df_merged.reset_index(inplace=True)
#%%
# save into nc
df_merged['crs'] = int(0)

df_xarray = df_merged.to_xarray()
df_xarray.to_netcdf('../Outputs/pr__cum_loss.nc')

#%%
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Set the same color limits for all three plots
color_min = min(df_merged[['cum loss 20_21', 'cum loss 20', 'cum loss 20_21_22']].min())
color_max = max(df_merged[['cum loss 20_21', 'cum loss 20', 'cum loss 20_21_22']].max())

# Create subplots with 1 row and 3 columns
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Scatter plot for cum loss 20
scatter_20 = axes[0].scatter(df_merged['lon'], df_merged['lat'], c=df_merged['cum loss 20'], cmap='PuOr', vmin=color_min, vmax=color_max)
axes[0].set_title('Cumulative Loss (20)')
axes[0].set_yticks([])
axes[0].set_xticks([])

# Scatter plot for cum loss 20_21
scatter_20_21 = axes[1].scatter(df_merged['lon'], df_merged['lat'], c=df_merged['cum loss 20_21'], cmap='PuOr', vmin=color_min, vmax=color_max)
axes[1].set_title('Cumulative Loss (20-21)')
axes[1].set_yticks([])
axes[1].set_xticks([])

# Scatter plot for cum loss 20_21_22
scatter_20_21_22 = axes[2].scatter(df_merged['lon'], df_merged['lat'], c=df_merged['cum loss 20_21_22'], cmap='PuOr', vmin=color_min, vmax=color_max)
axes[2].set_title('Cumulative Loss (20-21-22)')
axes[2].set_yticks([])  # Remove y-axis labels
axes[2].set_xticks([])

# Create a common colorbar
divider = make_axes_locatable(axes[-1])
cax = divider.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(scatter_20_21_22, cax=cax, label='Cumulative Loss')

# Adjust layout for better spacing
plt.tight_layout()

# Show the plots
plt.show()