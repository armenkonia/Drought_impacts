# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 09:43:18 2023

@author: armen
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

os.chdir(r"C:\Users\armen\OneDrive - UCLA IT Services\UCLA Projects\COEQWAL")
# os.chdir(r"C:\Users\armen\Desktop\Drought Impacts - Final\Drought Declaration")
#%%
landiq_2014 = pd.read_pickle('Data\Pickle\landiq_hr.pk')[0].to_crs('epsg:3857')
landiq_2016 = pd.read_pickle('Data\Pickle\landiq_hr.pk')[1].to_crs('epsg:3857')
landiq_2018 = pd.read_pickle('Data\Pickle\landiq_hr.pk')[2].to_crs('epsg:3857')
landiq_2019 = pd.read_pickle('Data\Pickle\landiq_hr.pk')[3].to_crs('epsg:3857')
landiq_2020 = pd.read_pickle('Data\Pickle\landiq_hr.pk')[4].to_crs('epsg:3857')
landiq_2021 = pd.read_pickle('Data\Pickle\landiq_hr.pk')[5].to_crs('epsg:3857')
landiq_2022 = pd.read_pickle('Data\Pickle\landiq_hr.pk')[6].to_crs('epsg:3857')
landiq_2016.rename(columns={'Acres': 'ACRES'}, inplace=True)


#%%
# Classify land ag, urban or fallow based on crop type 
def classify_land(landiq):
    new_landiq = landiq.copy()
    new_landiq['TYPE'] = np.nan
    new_landiq.loc[new_landiq['CLASS2'].isin(['G', 'R', 'F', 'P','T', 'D', 'C', 'V', 'S', 'YP']), 'TYPE'] = 'Agriculture'
    new_landiq.loc[new_landiq['CLASS2'].isin(['U', 'UR', 'UC', 'UI','UV','UL']), 'TYPE'] = 'Urban'
    new_landiq.loc[new_landiq['CLASS2'].isin(['I','X']), 'TYPE'] = 'Fallow'
    new_landiq.loc[new_landiq['CLASS2'].isin(['NR']), 'TYPE'] = 'Natural Lands'
    new_landiq['TYPE'].fillna('Other', inplace=True)
    
    return new_landiq

landiq_2016_classified = classify_land(landiq_2016)
landiq_2018_classified = classify_land(landiq_2018)
landiq_2020_classified = classify_land(landiq_2020)
landiq_2021_classified = classify_land(landiq_2021)
landiq_2022_classified = classify_land(landiq_2022)


#%%
def calculate_land_area_HR (column_name, land_type):
    
    # This function filters a DataFrame based on a specified land type. 
    # If the type is 'All', it returns the original DataFrame; otherwise, it returns only the land type selected
    def filter_by_land_type(landiq_df, land_type):
        if land_type == 'All':
            return landiq_df
        else:
            return landiq_df.loc[landiq_df['TYPE'] == land_type]
    
    landiq_2016_lt = filter_by_land_type(landiq_2016_classified, land_type)
    landiq_2018_lt = filter_by_land_type(landiq_2018_classified, land_type)
    landiq_2020_lt = filter_by_land_type(landiq_2020_classified, land_type)
    landiq_2021_lt = filter_by_land_type(landiq_2021_classified, land_type)
    landiq_2022_lt = filter_by_land_type(landiq_2022_classified, land_type)

    # Calculate the area for each classification
    total_area_16 = landiq_2016_lt.groupby([column_name]).sum(numeric_only=True)['ACRES']
    total_area_18 = landiq_2018_lt.groupby([column_name]).sum(numeric_only=True)['ACRES']
    total_area_20 = landiq_2020_lt.groupby([column_name]).sum(numeric_only=True)['ACRES']
    total_area_21 = landiq_2021_lt.groupby([column_name]).sum(numeric_only=True)['ACRES']
    total_area_22 = landiq_2022_lt.groupby([column_name]).sum(numeric_only=True)['ACRES']

    # Merge the series
    total_area_merged=pd.concat([total_area_16,total_area_18,total_area_20,total_area_21,total_area_22],axis=1)
    total_area_merged.columns = ['Field_2016','Field_2018','Field_2020','Field_2021','Field_2022']

    # Calculate the total for each year
    sums = total_area_merged[['Field_2016', 'Field_2018','Field_2020', 'Field_2021','Field_2022']].sum()
    
    # Rename the index
    total_area_merged.loc[len(total_area_merged.index)] = {'Field_2016': sums['Field_2016'], 'Field_2018': sums['Field_2018'], 'Field_2020': sums['Field_2020'], 'Field_2021': sums['Field_2021'], 'Field_2022': sums['Field_2022']}
    if column_name == 'TYPE':
         row_n = 3
    elif column_name == 'HR_NAME':
         row_n = 10
    
    total_area_merged = total_area_merged.rename(index={row_n: 'Total'})

    # Calculate the percent change and difference in area
    total_area_merged['pct_change_str'] = ((total_area_merged[['Field_2016', 'Field_2022']].pct_change(axis=1)['Field_2022']) * 100).round(2).map(str) + '%'
    total_area_merged ['Difference'] = np.abs(total_area_merged['Field_2016'] - total_area_merged['Field_2022'])
    
    total_area_plot =pd.concat([total_area_16,total_area_18,total_area_20,total_area_21,total_area_22],axis=1)
    total_area_plot.columns = ['Field_2016','Field_2018','Field_2020','Field_2021','Field_2022']
    # Create a transposed dataframe for plotting
    total_area_plot = total_area_plot.transpose()
    
    return total_area_merged, total_area_plot

total_area_all, total_area_plot_all = calculate_land_area_HR('HR_NAME', 'All')
total_area_ag, total_area_plot_ag = calculate_land_area_HR('HR_NAME', 'Agriculture')
total_area_ub, total_area_plot_ub = calculate_land_area_HR('HR_NAME', 'Urban')
total_area_fl, total_area_plot_fl = calculate_land_area_HR('HR_NAME', 'Fallow')
total_area_nl, total_area_plot_nl = calculate_land_area_HR('HR_NAME', 'Natural Lands')

#%%

def calculate_crops_area_hr(landiq_classified, column='CLASS2'):
    """
    Calculate the crop areas in different hydrologic regions.

    Parameters:
    - landiq_classified: DataFrame containing land IQ data.
    - column: based on which column the class is needed

    Returns:
    - crops_area_all_hr: DataFrame containing the calculated crop areas.
    """
    landiq_classified = landiq_classified[landiq_classified['TYPE'] == 'Agriculture']
    crops_area_all_hr = pd.DataFrame()

    for hr_region in landiq_classified['HR_NAME'].unique():
        crops_hr = landiq_classified[landiq_classified['HR_NAME'] == hr_region]
        crops_area_hr = crops_hr.groupby([column]).sum(numeric_only=True)['ACRES']
        crops_area_all_hr = pd.concat([crops_area_all_hr, crops_area_hr], axis=1)

    crops_area_all_hr.columns = landiq_classified['HR_NAME'].unique()
    # Remove columns with the name 'None'
    crops_area_all_hr = crops_area_all_hr.loc[:, crops_area_all_hr.columns.notnull()]

    return crops_area_all_hr

landiq_2016_crops = calculate_crops_area_hr(landiq_2016_classified)
landiq_2018_crops = calculate_crops_area_hr(landiq_2018_classified)
landiq_2020_crops = calculate_crops_area_hr(landiq_2020_classified)
landiq_2021_crops = calculate_crops_area_hr(landiq_2021_classified)
landiq_2022_crops = calculate_crops_area_hr(landiq_2022_classified)

landiq_2016_crops_sublass = calculate_crops_area_hr(landiq_2016_classified, column='CROPTYP2')
landiq_2018_crops_sublass = calculate_crops_area_hr(landiq_2018_classified, column='CROPTYP2')
landiq_2020_crops_sublass = calculate_crops_area_hr(landiq_2020_classified, column='CROPTYP2')
landiq_2021_crops_sublass = calculate_crops_area_hr(landiq_2021_classified, column='CROPTYP2')
landiq_2022_crops_sublass = calculate_crops_area_hr(landiq_2022_classified, column='CROPTYP2')
#%%

merged_crops = pd.concat([landiq_2016_crops, 
                          landiq_2018_crops, 
                          landiq_2020_crops, 
                          landiq_2021_crops, 
                          landiq_2022_crops], axis=1, keys=['2016', '2018', '2020', '2021', '2022'])
merged_crops_sublass = pd.concat([landiq_2016_crops_sublass, 
                          landiq_2018_crops_sublass, 
                          landiq_2020_crops_sublass, 
                          landiq_2021_crops_sublass,
                          landiq_2022_crops_sublass], axis=1, keys=['2016', '2018', '2020', '2021', '2022'])
#%%

#%%
# The code creates a lists for each HR. The rows of each element correspond to different crops, and the columns represent different years
all_hr_crops = list()
for hr_region in landiq_2016_classified['HR_NAME'].unique():
    hr_crop = merged_crops.iloc[:, merged_crops.columns.get_level_values(1)==hr_region]
    # hr_crop.columns = hr_crop.columns.droplevel(1)
    all_hr_crops.append(hr_crop)
    
#%%
# save both files
loaded_object = [landiq_2016_crops,landiq_2018_crops,landiq_2020_crops,landiq_2021_crops,landiq_2022_crops, all_hr_crops]
# open a file, where you ant to store the data
with open('Data\Pickle\crop_area_HR.pk', 'wb') as file:
    pickle.dump(loaded_object, file)
    #%%

loaded_object = [total_area_all, total_area_ag, total_area_ub, total_area_fl, total_area_nl]
# open a file, where you ant to store the data
with open('Data\land_area_HR.pk', 'wb') as file:
    pickle.dump(loaded_object, file)
    #%%
merged_crops_sublass.to_csv('Data\crop areas with subclassification.csv')
