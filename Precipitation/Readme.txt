Average precipitation:
1 - obtain pr normalized
This script calculates cumulative monthly precipitation from daily data. Then, using the monthly data, it computes the cumulative precipitation for each water year.

2 - obtain prcp_cum_loss
This script calculates the mean precipitation for all water years and then normalizes the precipitation for each individual year (X_given_month/X_mean). Additionally, it multiplies the average precipitation by 2 and then takes the sum of the precipitation for 2020 and 2021 for each grid cell. This sum is then divided by the average precipitation multiplied by 2 to further analyze precipitation patterns. Same process for 20-21-22

3 - plot of perc of av pr


Percentile precipitation:

1 - calculating pr percentiles.py
2 - save all HR percentile files to one NC file.py
3 - plot_pr_percentile.ipynb