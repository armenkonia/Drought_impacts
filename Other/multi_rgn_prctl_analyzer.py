#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 3 16:53:31 2023
@author: alvar
"""

import pandas as pd
import geopandas as gpd
import rasterio as rio
import xarray as xr
import numpy as np
from percentile_average_function import func_for_tperiod
from tqdm import tqdm
import time

#%%
shape_path_filename = r"..\Datasets\HRs\i03_Hydrologic_Regions.shp"
hrs = gpd.read_file(shape_path_filename).to_crs("EPSG:4326")
# hrs = hrs[hrs['HR_NAME'] == 'Sacramento River']

minx, miny, maxx, maxy = hrs.geometry.total_bounds
#%%
input_folder = '../Datasets/pr'

prec_df = pd.DataFrame()
for year_n in range(1990,2023):
    filepath = input_folder +'/pr_' + '%s' %(year_n) + '.nc'
    ds = xr.open_dataset(filepath)
    da = ds["precipitation_amount"].sel(lon=slice(minx, maxx),lat=slice(maxy, miny))
    da_monthly =da.groupby('day.month').sum('day')
    da_monthly = da_monthly.rio.write_crs("EPSG:4326")
    da_clip = da_monthly.rio.clip(hrs.geometry)
    df = da_clip.to_dataframe().reset_index()
    df['year'] = year_n
    df['date'] = pd.to_datetime(dict(year=df.year, month=df.month, day=1))
    df['cell'] = df.lon.astype(str) + "_" + df.lat.astype(str)
    prec_df = pd.concat([prec_df,df]).reset_index(drop=True)
    print(year_n)
    
#%%
unique_cells = np.unique(prec_df['cell'])

start_time = time.time()
print (start_time)

percentile = pd.DataFrame()
for i in tqdm(unique_cells):
    one_cell = prec_df.loc[prec_df.cell == i]
    if one_cell.precipitation_amount.isna().any()==True:
        pass
    
    else:
        one_cell_perc = func_for_tperiod(one_cell, 
                            date_column = 'date', value_column = 'precipitation_amount', 
                            input_timestep = 'M', analysis_period = '1Y',
                            function = 'percentile', grouping_column='cell',
                            correcting_no_reporting = False, correcting_column = 'capacity',
                            baseline_start_year = 1991, baseline_end_year = 2020,
                            remove_zero = False)

        percentile = pd.concat([percentile, one_cell_perc])

end_time = time.time()
total_elapsed_time = (end_time - start_time)/60
print(f"Total Elapsed Time: {total_elapsed_time:.1f}min")


#%%
percentile.to_csv("../trial outputs/pr_percentile.csv")
percentile.set_index(['lat','lon','date'], inplace=True)
df_new_xarray = percentile.to_xarray()
df_new_xarray.to_netcdf("../trial outputs/pr_percentile.nc")