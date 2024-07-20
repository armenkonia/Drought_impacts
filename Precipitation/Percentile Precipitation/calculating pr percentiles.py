# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:18:19 2024

@author: armen
"""

import pandas as pd
import geopandas as gpd
import rasterio as rio
import xarray as xr
import numpy as np
from percentile_average_function import func_for_tperiod
from tqdm import tqdm
import time
import os

def get_region_percentile (frequency = '2Y',hr = 'Sacramento River', baseline_start_year = 1991, baseline_end_year = 2020, analysis_start_year = 1987, analysis_end_year = 2024,
                           input_directory = '../../Datasets/pr', hr_directory = r"../../Datasets/HRs/i03_Hydrologic_Regions.shp", output_directory = '../../Outputs/all_regions_2yr_percentile/',
                           ):
    hrs = gpd.read_file(hr_directory).to_crs("EPSG:4326")
    hrs = hrs[hrs['HR_NAME'] == hr]
    minx, miny, maxx, maxy = hrs.geometry.total_bounds    
    
    input_folder = input_directory
    prec_df = pd.DataFrame()
    for year_n in range(analysis_start_year,analysis_end_year): 
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
        # print(year_n)
        
    
    unique_cells = np.unique(prec_df['cell'])
    
    percentile = pd.DataFrame()
    for i in tqdm(unique_cells):
        one_cell = prec_df.loc[prec_df.cell == i]
        if one_cell.precipitation_amount.isna().any()==True:
            pass
        
        else:
            one_cell_perc = func_for_tperiod(one_cell, 
                                date_column = 'date', value_column = 'precipitation_amount', 
                                input_timestep = 'M', analysis_period = frequency,
                                function = 'percentile', grouping_column='cell',
                                correcting_no_reporting = False, correcting_column = 'capacity',
                                baseline_start_year = baseline_start_year, baseline_end_year = baseline_end_year,
                                remove_zero = False)
    
            percentile = pd.concat([percentile, one_cell_perc])
        
    os.makedirs(output_directory, exist_ok=True)
    # prec_df.to_csv(f"{output_directory}/{hr}_pr_data.csv")
    percentile.to_csv(f"{output_directory}/{hr}_pr_percentile.csv")
    percentile.set_index(['lat','lon','date'], inplace=True)
    df_xarray = percentile.to_xarray()
    df_xarray.to_netcdf(f"{output_directory}/{hr}_pr_percentile.nc")
    
    return percentile

shape_path_filename = r"../../Datasets/HRs/i03_Hydrologic_Regions.shp"
hrs = gpd.read_file(shape_path_filename).to_crs("EPSG:4326")
hr_regions = hrs['HR_NAME'].unique()

prctl_hr_rgns = []
for hr in hr_regions:
    prctl  = get_region_percentile(frequency = '1Y',hr = hr, baseline_start_year = 2018, baseline_end_year = 2020, analysis_start_year = 2016, analysis_end_year = 2021,
                                            input_directory = '../../Datasets/pr', hr_directory = r"../../Datasets/HRs/i03_Hydrologic_Regions.shp", 
                                            output_directory = '../../trial outputs/all_regions_1yr_percentile/' 
                                            )
    prctl_hr_rgns.append (prctl)

      
prctl_hr_rgns = []
for hr in hr_regions:
    prctl  = get_region_percentile(frequency = '2Y',hr = hr, baseline_start_year = 2018, baseline_end_year = 2020, analysis_start_year = 2016, analysis_end_year = 2021,
                                            input_directory = '../../Datasets/pr', hr_directory = r"../../Datasets/HRs/i03_Hydrologic_Regions.shp", output_directory = '../../trial outputs/all_regions_2yr_percentile/' 
                                            )
    prctl_hr_rgns.append (prctl)


prctl_hr_rgns = []
for hr in hr_regions:
    prctl  = get_region_percentile(frequency = '3Y',hr = hr, baseline_start_year = 2018, baseline_end_year = 2020, analysis_start_year = 2016, analysis_end_year = 2021,
                                            input_directory = '../../Datasets/pr', hr_directory = r"../../Datasets/HRs/i03_Hydrologic_Regions.shp", 
                                            output_directory = '../../trial outputs/all_regions_3yr_percentile/' 
                                            )
    prctl_hr_rgns.append (prctl)
