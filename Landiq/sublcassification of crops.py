# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 20:18:28 2024

@author: armen
"""

import pandas as pd

# Define the data for each class type, including special '**' entries
data = {
    "G": {
        "Number": ["1", "2", "3", "6", "7", "**"],
        "Description": ["Barley", "Wheat", "Oats", "Miscellaneous grain and hay", "Mixed grain and hay", "No subclass"],
        "Class_Description": ["Grain and hay crops"] * 6
    },
    "R": {
        "Number": ["1", "2", "**"],
        "Description": ["Rice", "Wild Rice", "No subclass"],
        "Class_Description": ["Rice"] * 3
    },
    "F": {
        "Number": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "**"],
        "Description": ["Cotton", "Safflower", "Flax", "Hops", "Sugar beets", "Corn (field & sweet)", "Grain sorghum", "Sudan", "Castor beans", "Beans (dry)", "Miscellaneous field", "Sunflowers", "Hybrid sorghum/sudan", "Millet", "Sugar cane", "Corn, Sorghum or Sudan grouped for remote sensing only", "No subclass"],
        "Class_Description": ["Field crops"] * 17
    },
    "P": {
        "Number": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "**"],
        "Description": ["Alfalfa & alfalfa mixtures", "Clover", "Mixed pasture", "Native pasture", "Induced high water table native pasture", "Miscellaneous grasses", "Turf farms", "Bermuda grass", "Rye grass", "Klein grass", "No subclass"],
        "Class_Description": ["Pasture"] * 11
    },
    "T": {
        "Number": ["1", "2", "3", "4", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "**"],
        "Description": ["Artichokes", "Asparagus", "Beans (green)", "Cole crops (mixture of 22-25)", "Carrots", "Celery", "Lettuce (all types)", "Melons, squash, and cucumbers (all types)", "Onions & garlic", "Peas", "Potatoes", "Sweet potatoes", "Spinach", "Tomatoes (processing)", "Flowers, nursery & Christmas tree farms", "Mixed (four or more)", "Miscellaneous truck", "Bush berries", "Strawberries", "Peppers (chili, bell, etc.)", "Broccoli", "Cabbage", "Cauliflower", "Brussels sprouts", "Tomatoes (market)", "Greenhouse", "Blueberries", "Asian leafy vegetables", "Lettuce or Leafy Greens grouped for remote sensing only", "Potato or Sweet potato grouped for remote sensing only", "No subclass"],
        "Class_Description": ["Truck, nursery & berry crops"] * 31
    },
    "D": {
        "Number": ["1", "2", "3", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "**"],
        "Description": ["Apples", "Apricots", "Cherries", "Peaches and nectarines", "Pears", "Plums", "Prunes", "Figs", "Miscellaneous deciduous", "Mixed deciduous", "Almonds", "Walnuts", "Pistachios", "Pomegranates", "Plums, Prunes or Apricots grouped for remote sensing only", "No subclass"],
        "Class_Description": ["Deciduous fruits and nuts"] * 16
    },
    "C": {
        "Number": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "**"],
        "Description": ["Grapefruit", "Lemons", "Oranges", "Dates", "Avocados", "Olives", "Miscellaneous subtropical fruit", "Kiwis", "Jojoba", "Eucalyptus", "Mixed subtropical fruits", "No subclass"],
        "Class_Description": ["Citrus and subtropical"] * 12
    },
    "V": {
        "Number": ["1", "2", "3", "**"],
        "Description": ["Table grapes", "Wine grapes", "Raisin grapes", "No subclass"],
        "Class_Description": ["Vineyards"] * 4
    },
    "YP": {
        "Number": ["**"],
        "Description": ["No subclass"],
        "Class_Description": ["Young Perennial"] * 1
    },
    "I": {
        "Number": ["1", "2", "4", "**"],
        "Description": ["Land not cropped the current or previous crop season, but cropped within the past three years", "New lands being prepared for crop production", "Long term, land consistently idle for four or more years", "No subclass"],
        "Class_Description": ["Idle"] * 4
    },
    "X": {
        "Number": ["**"],
        "Description": ["Not cropped or unclassified"],
        "Class_Description": ["Not cropped or unclassified"] * 1
    },
    "S": {
        "Number": ["1", "2", "3", "4", "5", "6", "**"],
        "Description": ["Farmsteads (includes a farm residence)", "Livestock feed lot operations", "Dairies", "Poultry farms", "Farmsteads (without a farm residence)", "Miscellaneous semi-agricultural (small roads, ditches, non-planted areas of cropped fields)", "No subclass"],
        "Class_Description": ["Semi-agricultural & incidental to agriculture"] * 7
    },
    "U": {
        "Number": ["**"],
        "Description": ["Urban - generic nomenclature with no subclass"],
        "Class_Description": ["Urban"] * 1
    },
    "UR": {
        "Number": ["1", "2", "3", "4","11", "12", "13", "14","21", "22", "23", "24","31", "32", "33", "34","41", "42", "43", "44"],
        "Description": ["Single family dwellings with lot sizes greater than 1 acre up to 5 acres.","Single family dwellings with a density of 1 unit/acre up to 8+ units per acre.","Multiple family (apartments, condominiums, townhouses, barracks, bungalows, duplexes, etc.).","Trailer courts.","0% to 25% area irrigated.","26% to 50% area irrigated.","51% to 75% area irrigated.","76% to 100% area irrigated.","0% to 25% area irrigated.","26% to 50% area irrigated.","51% to 75% area irrigated.","76% to 100% area irrigated.","0% to 25% area irrigated.","26% to 50% area irrigated.","51% to 75% area irrigated.","76% to 100% area irrigated.","0% to 25% area irrigated.","26% to 50% area irrigated.","51% to 75% area irrigated.","76% to 100% area irrigated."],
        "Class_Description": ["Urban residential"] * 20
    },
    "UC": {
        "Number": ["1", "2", "3", "4", "5", "6", "7", "8", "**"],
        "Description": ["Offices, retailers, etc.", "Hotels", "Motels", "Recreation vehicle parking, camp sites", "Institutions (hospitals, prisons, reformatories, asylums, etc., having a reasonably constant 24-hour resident population)", "Schools (yards to be mapped separately if large enough)", "Municipal auditoriums, theaters, churches, buildings and stands associated with race tracks, football stadiums, baseball parks, rodeo arenas, amusement parks, etc.", "Miscellaneous highwater use (to be used to indicate a high water use condition not covered by the above categories.)", "No subclass"],
        "Class_Description": ["Commercial"] * 9
    },
    "UI": {
        "Number": ["1", "2", "3", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "**"],
        "Description": ["Manufacturing, assembling, and general processing", "Extractive industries (oil fields, rock quarries, gravel pits, rock and gravel processing plants, etc.)", "Storage and distribution (warehouses, substations, railroad marshalling yards, tank farms, etc.)", "Saw mills", "Oil refineries", "Paper mills", "Meat packing plants", "Steel and aluminum mills", "Fruit and vegetable canneries and general food processing", "Miscellaneous highwater use (to be used to indicate a high water use condition not covered by other categories.)", "Sewage treatment plant including ponds", "Waste accumulation sites (public dumps, sewage sludge sites, landfill and hazardous waste sites, etc.)", "Wind farms, solar collector farms, etc.", "No subclass"],
        "Class_Description": ["Industrial"] * 14
    },
    "UL": {
        "Number": ["1", "2", "3", "4", "5", "**"],
        "Description": ["Lawn area – irrigated", "Golf course – irrigated", "Ornamental landscape (excluding lawns) – irrigated", "Cemeteries – irrigated", "Cemeteries – not irrigated", "No subclass"],
        "Class_Description": ["Urban landscape"] * 6
    },
    "UV": {
        "Number": ["1", "3", "4", "6", "7", "**"],
        "Description": ["Unpaved areas (vacant lots, graveled surfaces, play yards, developable open lands within urban areas, etc.)", "Railroad right of way", "Paved areas (parking lots, paved roads, oiled surfaces, flood control channels, tennis court areas, auto sales lots, etc.)", "Airport runways", "Land in urban area that is not developable", "No subclass"],
        "Class_Description": ["Vacant"] * 6
    },
    "NC": {
        "Number": ["**"],
        "Description": ["Native class - generic nomenclature with no subclass"],
        "Class_Description": ["Native class"] * 1
    },
    "NV": {
        "Number": ["1", "2", "3", "4", "5", "6", "7", "**"],
        "Description": ["Grassland", "Light brush", "Medium brush", "Heavy brush", "Brush and timber", "Forest", "Oak woodland", "No subclass"],
        "Class_Description": ["Native vegetation"] * 8
    },
    "NR": {
        "Number": ["1", "2", "3", "4", "5", "**"],
        "Description": ["Marsh lands, tules and sedges", "Natural highwater table meadow", "Trees, shrubs or other larger stream side or watercourse vegetation", "Seasonal duck marsh, dry or only partially wet during summer", "Permanent duck marsh, flooded during summer", "No subclass"],
        "Class_Description": ["Riparian vegetation"] * 6
    },
    "NW": {
        "Number": ["1", "2", "3", "4", "5", "6", "7", "**"],
        "Description": ["River or stream (natural fresh water channels)", "Water channel (all sizes - ditches and canals - delivering water for irrigation and urban use)", "Water channel (all sizes - ditches and canals - for removing on-farm drainage water)", "Freshwater lake, reservoir, or pond (all sizes)", "Brackish and saline water (includes areas in estuaries, inland water bodies, the ocean, etc.)", "Wastewater pond (dairy, sewage, cannery, winery, etc.)", "Paved water conveyance channels within urban areas (mainly for flood control)", "No subclass"],
        "Class_Description": ["Water surface"] * 8
    },
    "NB": {
        "Number": ["1", "2", "3", "4", "5", "**"],
        "Description": ["Dry stream channels", "Mine tailings", "Barren land", "Salt flats", "Sand dunes", "No subclass"],
        "Class_Description": ["Barren and Wasteland"] * 6
    },
    "E": {
        "Number": ["**"],
        "Description": ["Entry denied - no subclass"],
        "Class_Description": ["Entry denied"] * 1
    },
    "Z": {
        "Number": ["**"],
        "Description": ["Outside of study area - no subclass"],
        "Class_Description": ["Outside of study area"] * 1
    }
}

# Create a single DataFrame with class type included
dfs = []
for class_type, details in data.items():
    df = pd.DataFrame(details)
    df["Class"] = class_type
    dfs.append(df)

# Concatenate all DataFrames into one
merged_df = pd.concat(dfs, ignore_index=True)
merged_df = merged_df[['Class', 'Class_Description', 'Number', 'Description']]
merged_df['Number_cleaned'] = merged_df['Number'].replace('**', '')
merged_df['CROPTYP2'] = merged_df['Class'] + merged_df['Number_cleaned']
merged_df.loc[merged_df['Description'] == "No subclass", 'Description'] = " No subclass - " + merged_df['Class_Description']
#%%
mapping_dict = merged_df.set_index('CROPTYP2')['Description'].to_dict()

crop_areas = pd.read_csv('subclassified_crop_areas.csv', header=[0, 1], index_col=0)
crop_areas.index = crop_areas.index.to_series().map(mapping_dict)

# tulare_lake_df = crop_areas.xs('Tulare Lake', axis=1, level=1)
# sacramento_river_df = crop_areas.xs('Sacramento River', axis=1, level=1)
# san_joaquin_river_df = crop_areas.xs('San Joaquin River', axis=1, level=1)
# selected_areas_df = pd.concat([tulare_lake_df, sacramento_river_df, san_joaquin_river_df], axis=1)

selected_columns = [col for col in crop_areas.columns if col[1] in ['Tulare Lake', 'San Joaquin River', 'Sacramento River']]
selected_areas_df = crop_areas[selected_columns]

annual_sums = crop_areas.groupby(level=0, axis=1).sum()
