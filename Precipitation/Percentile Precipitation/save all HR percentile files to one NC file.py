# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 18:03:02 2024

@author: armen
"""

import os
import geopandas as gpd
import pandas as pd

folder_path = r"C:\Users\armen\Desktop\Drought Impacts\trial outputs\all_regions_1yr_percentile"

prctl_hr_rgns_dict = {}
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        file_key = os.path.splitext(filename)[0]
        prctl_hr_rgns_dict[file_key] = pd.read_csv(file_path, usecols=lambda column: column != 'Unnamed: 0')

merged_df = pd.concat(prctl_hr_rgns_dict.values(), ignore_index=True)
merged_df.set_index(['lat', 'lon', 'date'], inplace=True)
df_xarray = merged_df.to_xarray()
df_xarray.to_netcdf('../../trial outputs/all_regions_1yr_percentile/CA_1_yr_percentile.nc')


folder_path = r"C:\Users\armen\Desktop\Drought Impacts\trial outputs\all_regions_2yr_percentile"

prctl_hr_rgns_dict = {}
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        file_key = os.path.splitext(filename)[0]
        prctl_hr_rgns_dict[file_key] = pd.read_csv(file_path, usecols=lambda column: column != 'Unnamed: 0')

merged_df = pd.concat(prctl_hr_rgns_dict.values(), ignore_index=True)
merged_df.set_index(['lat', 'lon', 'date'], inplace=True)
df_xarray = merged_df.to_xarray()
df_xarray.to_netcdf('../../trial outputs/all_regions_2yr_percentile/CA_2_yr_percentile.nc')



folder_path = r"C:\Users\armen\Desktop\Drought Impacts\trial outputs\all_regions_3yr_percentile"

prctl_hr_rgns_dict = {}
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        file_key = os.path.splitext(filename)[0]
        prctl_hr_rgns_dict[file_key] = pd.read_csv(file_path, usecols=lambda column: column != 'Unnamed: 0')

merged_df = pd.concat(prctl_hr_rgns_dict.values(), ignore_index=True)
merged_df.set_index(['lat', 'lon', 'date'], inplace=True)
df_xarray = merged_df.to_xarray()
df_xarray.to_netcdf('../../trial outputs/all_regions_3yr_percentile/CA_3_yr_percentile.nc')
