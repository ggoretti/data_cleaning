# -*- coding: utf-8 -*-
"""
@author: Gianni Goretti
"""

# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
#     DATA IMPORT
# =============================================================================

# Wind turbine data
data_raw = pd.read_csv("input_data.csv", index_col=0, parse_dates=True)
data_raw.sort_index(inplace = True)
print(data_raw.columns)

wtn = 15  # number of turbines




# =============================================================================
#     EXPLORATORY ANALYSIS
# =============================================================================

# List of wind speed column names
windSpeed_cols = ['windSpeed_wt' + str(wt).zfill(2) for wt in range(1,wtn+1)]  # turbine wind speed
    
# List of power column names
power_cols = ['power_wt' + str(wt).zfill(2) for wt in range(1,wtn+1)]  # turbine active power
    
# - - - Calculate wind farm statistics - - - 
# Average wind speed
data_raw['windSpeed_avg'] = data_raw[windSpeed_cols].mean(axis=1, skipna=False)
# Standard deviation of wind speed
data_raw['windSpeed_std'] = data_raw[windSpeed_cols].std(axis=1, skipna=False)
# Average power output
data_raw['power_avg'] = data_raw[power_cols].mean(axis=1, skipna=False)


# - - - Power curve with average wind farm values - - -
plt.figure()
plt.scatter(data_raw['windSpeed_avg'], data_raw['power_avg'], c=data_raw['windSpeed_std'], cmap='plasma', edgecolor='k', alpha=0.9)
plt.xlabel('average wind speed [m/s]'); plt.ylabel('normalised average power [p.u.]')
plt.title('Power curve - Raw data')
plt.grid(ls='--', lw=0.5, c='grey')
plt.tight_layout()
plt.show()


# Define power curve's wind speeds
ws_cut_in=2.0  # cut-in wind speed
ws_rated=11.5  # rated wind speed
ws_cut_out=22.0  # cut-out wind speed

# Add lines to plot
plt.axvline(ws_cut_in, ls='--', lw=1.5, c='k')
plt.axvline(ws_rated, ls='--', lw=1.5, c='k')
plt.axvline(ws_cut_out, ls='--', lw=1.5, c='k')




# =============================================================================
#     DATA CLEANING
# =============================================================================

# Clean data excluding anomalous (i.e. flagged) data
data_norm = clean_data(data_raw, wtn, 2.0, 11.5, 22.0)

# Clean data including anomalous (i.e. flagged) data
data_flag = clean_data(data_raw, wtn, 2.0, 11.5, 22.0, anomalous=True)

# Re-calculate wind farm statistics
data_test['windSpeed_avg'] = data_test[windSpeed_cols].mean(axis=1, skipna=False)
data_test['power_avg'] = data_test[power_cols].mean(axis=1, skipna=False)
print(data_test['power_avg'].describe())
powerCurve(data_test, 15)
plt.title(r"Anomalous = $\bf{False}$")
plt.savefig('Figures/clean_unflag.jpg', dpi=600)


data_flags['windSpeed_avg'] = data_flags[windSpeed_cols].mean(axis=1, skipna=False)
data_flags['power_avg'] = data_flags[power_cols].mean(axis=1, skipna=False)
print(data_flags['power_avg'].describe())
powerCurve(data_flags, 15)
plt.title(r"Anomalous = $\bf{True}$")
plt.savefig('Figures/clean_anomal.jpg', dpi=600)



# Histogram
plt.figure()
plt.hist(data_flags.power_avg.dropna(), edgecolor='k', label='unflagged + anomalous', alpha=0.8)
plt.hist(data_test.power_avg.dropna(), edgecolor='k', label='unflagged', alpha=0.8)
plt.xlabel('normalised power [p.u.]'); plt.ylabel('count')
plt.title('Wind farm power distribution')
plt.legend(); plt.tight_layout()
plt.savefig('Figures/histograms.jpg', dpi=600)


# Boxplot
boxes = [data_test.power_avg.dropna(), data_flags.power_avg.dropna()]
boxprops = dict(linestyle='-', linewidth=2.5, color='k')
medianprops = dict(linewidth=2.0, color='b')
meanpointprops = dict(marker='D', markeredgecolor='black', markerfacecolor='b')
plt.figure()
plt.boxplot(boxes, showmeans=True, vert=False, 
            boxprops=boxprops, medianprops=medianprops, meanprops=meanpointprops)
plt.yticks([1,2], ['unflagged', 'unflagged + \nanomalous  '], fontsize=16, ha='right')
plt.xlabel('normalised power [p.u.]')
plt.title('Wind farm power distribution')
plt.tight_layout()
plt.savefig('Figures/boxplots.jpg', dpi=600)






