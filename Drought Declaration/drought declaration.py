# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 17:16:55 2024

@author: armen
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
ca_boundary = gpd.read_file('ca_state_boundary/ca_state_boundaries.shp')
county_boundaries = gpd.read_file('ca_county_boundaries/ca_county_boundaries.shp')
hr_shapes = gpd.read_file('../Datasets/HRs/i03_Hydrologic_Regions.shp')

# ca_boundary.crs = None
# county_boundaries.crs = None
# hr_shapes.crs = None
# county_boundaries.crs = 'EPSG:4326'

print("CRS of gpd_ca_boundary:", ca_boundary.crs)
print("CRS of county_boundaries:", county_boundaries.crs)
print("CRS of county_boundaries:", hr_shapes.crs)

#%%
# Create a figure and axis object
fig, ax = plt.subplots(figsize=(5, 5))

ca_boundary.plot(ax=ax, color='none')
county_boundaries.plot(ax=ax, color='none')
# hr_shapes.plot(ax=ax, color='none')


ax.set_title('California Boundary and County Boundaries')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.tight_layout()
plt.show()

#%%
county_boundaries['drought_declaration'] = None

# Update 'drought_declaration' column for Mendocino and Sonoma counties
county_boundaries.loc[county_boundaries['NAME'].isin(['Mendocino', 'Sonoma']), 'drought_declaration'] = 'April 21'

# Plot county boundaries
fig, ax = plt.subplots(figsize=(10, 10))
county_boundaries.plot(ax=ax, color='lightgray', edgecolor='black')

# Highlight counties with drought declaration on April 21
highlighted_counties = county_boundaries[county_boundaries['drought_declaration'] == 'April 21']
highlighted_counties.plot(ax=ax, color='red', edgecolor='black')

ax.set_title('County Boundaries with Drought Declaration')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.show()

#%%
# Define the watershed counties
counties_may10 = {
    'Klamath River Watershed': ['Del Norte', 'Humboldt', 'Modoc', 'Siskiyou', 'Trinity'],
    'Sacramento-San Joaquin Delta Watershed': ['Alameda', 'Alpine', 'Amador', 'Butte', 'Calaveras', 'Colusa', 'Contra Costa', 'El Dorado', 'Fresno', 'Glenn', 'Lake', 'Lassen', 'Madera', 'Mariposa', 'Merced', 'Modoc', 'Napa', 'Nevada', 'Placer', 'Plumas', 'Sacramento', 'San Benito', 'San Joaquin', 'Shasta', 'Sierra', 'Siskiyou', 'Solano', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity', 'Tuolumne', 'Yolo', 'Yuba'],
    'Tulare Lake Watershed': ['Fresno', 'Kern', 'Kings', 'Tulare']
}

# Convert the dictionary into a DataFrame
counties_may10_df = pd.DataFrame([(county, watershed) for watershed, counties in counties_may10.items() for county in counties], columns=['County', 'Watershed'])

county_boundaries.loc[county_boundaries['NAME'].isin([county for counties in counties_may10.values() for county in counties]), 'drought_declaration'] = 'May10'
#%%
counties_july8 = ['Inyo', 'Marin', 'Mono', 'Monterey', 'San Luis Obispo', 
                              'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz']
county_boundaries.loc[county_boundaries['NAME'].isin(counties_july8), 'drought_declaration'] = 'July 8'
#%%
county_boundaries['drought_declaration'].fillna('October 19', inplace=True)

#%%
declaration_dates = ['April 21, 2021', 'May10, 2021', 'July 8, 2021', 'October 19, 2021']

# Plot county boundaries
fig, ax = plt.subplots(1,4,figsize=(12, 4))
county_boundaries.plot(ax=ax[0], color='lightgray', edgecolor='black')
highlighted_counties = county_boundaries[county_boundaries['drought_declaration'] == 'April 21']
highlighted_counties.plot(ax=ax[0], color='red', edgecolor='black')
ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].set_title(f'{declaration_dates[0]}')

county_boundaries.plot(ax=ax[1], color='lightgray', edgecolor='black')
highlighted_counties = county_boundaries[county_boundaries['drought_declaration'].isin(['April 21', 'May10'])]
highlighted_counties.plot(ax=ax[1], color='red', edgecolor='black')
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_title(f'{declaration_dates[1]}')

county_boundaries.plot(ax=ax[2], color='lightgray', edgecolor='black')
highlighted_counties = county_boundaries[county_boundaries['drought_declaration'].isin(['April 21', 'May10','July 8'])]
highlighted_counties.plot(ax=ax[2], color='red', edgecolor='black')
ax[2].set_xticks([])
ax[2].set_yticks([])
ax[2].set_title(f'{declaration_dates[2]}')

county_boundaries.plot(ax=ax[3], color='lightgray', edgecolor='black')
highlighted_counties = county_boundaries[county_boundaries['drought_declaration'].isin(['April 21', 'May10','July 8','October 19'])]
highlighted_counties.plot(ax=ax[3], color='red', edgecolor='black')
ax[3].set_xticks([])
ax[3].set_yticks([])
ax[3].set_title(f'{declaration_dates[3]}')

fig.suptitle('Drought Declarations by County', fontsize=16)
plt.tight_layout()
plt.show()
#%%

