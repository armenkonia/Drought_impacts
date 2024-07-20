# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 12:59:57 2024

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


# filepath = r"C:\Users\armen\Desktop\Drought Impacts\Outputs\cum_pr_WY.nc"
# ds = xr.open_dataset(filepath)

# import HR regions
shape_path_filename = r"..\Datasets\HRs\i03_Hydrologic_Regions.shp"
hrs = gpd.read_file(shape_path_filename).to_crs("EPSG:4326")
hrs.HR_NAME
minx, miny, maxx, maxy = hrs.geometry.total_bounds

#%%
# open daily precp data, convert it to monthly and store it in a dataframe
input_folder = '../Datasets/pr'
df_merged = None  # Initialize an empty DataFrame
for year_n in range(1990,2023):
    filepath = input_folder +'/pr_' + '%s' %(year_n) + '.nc'
    ds = xr.open_dataset(filepath)
    da = ds["precipitation_amount"].sel(lon=slice(minx, maxx),lat=slice(maxy, miny))
    da_monthly =da.groupby('day.month').sum('day')
    da_monthly = da_monthly.rio.write_crs("EPSG:4326")
    da_clip = da_monthly.rio.clip(hrs.geometry)
    df = da_clip.to_dataframe()
    if df_merged is None:
        df_merged = df
    else:
        suffix = f'_{year_n}'
        df_merged = pd.merge(df_merged, df, left_index=True, right_index=True, suffixes=('', suffix))
    print(year_n)

# remove columns with crs
df_monthly_pr = df_merged.loc[:, ~df_merged.columns.str.startswith('crs')]
# rename columns with its corresponding year
df_monthly_pr.columns = list(range(1990,2023))
df_monthly_pr = df_monthly_pr.reset_index()

#%%
# melt all columns of df_normalized into a single column
df_single_column = df_monthly_pr.melt(id_vars=df_monthly_pr.columns[:3], var_name='Year', value_name='Precipitation')
df_single_column.set_index(df_single_column.columns[:4].tolist(), inplace=True)

#%%
# The following adds water year column and creates a dataframe for total pr per water year


df_single_column.reset_index(inplace=True)
# Convert 'Year' to datetime format
df_single_column['Year'] = pd.to_datetime(df_single_column['Year'], format='%Y')
# Create a new column for the water year (Water year starts from October 1st of the previous calendar year)
df_single_column['WaterYear'] = df_single_column['Year']
df_single_column['WaterYear'] = df_single_column['WaterYear'].dt.strftime('%Y')
df_single_column['WaterYear'] = df_single_column.apply(lambda row: str(int(row['WaterYear']) + 1) if row['month'] >= 10 else str(row['WaterYear']), axis=1)
# Group by lat, lon, and water_year, and sum the precipitation for each water year
df_water_yearly_sum = df_single_column.groupby(['lat', 'lon', 'WaterYear'])['Precipitation'].sum().reset_index()
# Set index
df_water_yearly_sum.set_index(['lat','lon','WaterYear'], inplace=True)
#%%
# save into nc
df_water_yearly_sum['crs'] = int(0)

df_xarray = df_water_yearly_sum.to_xarray()
df_xarray.to_netcdf('../Outputs/cum_pr_WY.nc')



