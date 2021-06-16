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

# Draw exploratory power curve with average wind farm values
powerCurve(data_raw, wtn)

# Define power curve's wind speeds
ws_cut_in=2.0  # cut-in wind speed
ws_rated=11.5  # rated wind speed
ws_cut_out=22.0  # cut-out wind speed

# Add lines to the power curve plot
plt.axvline(ws_cut_in, ls='--', lw=1.5, c='k')
plt.axvline(ws_rated, ls='--', lw=1.5, c='k')
plt.axvline(ws_cut_out, ls='--', lw=1.5, c='k')
plt.show()




# =============================================================================
#     DATA CLEANING
# =============================================================================

# Clean data excluding anomalous (i.e. flagged) data
data_norm = clean_data(data_raw, wtn, 2.0, 11.5, 22.0)

# Clean data including anomalous (i.e. flagged) data
data_flag = clean_data(data_raw, wtn, 2.0, 11.5, 22.0, anomalous=True)




# =============================================================================
#     DATA ANALYSIS
# =============================================================================

# Re-calculate wind farm statistics
data_norm['windSpeed_avg'] = data_norm[windSpeed_cols].mean(axis=1, skipna=False)
data_norm['power_avg'] = data_norm[power_cols].mean(axis=1, skipna=False)
print(data_norm['power_avg'].describe())

data_flag['windSpeed_avg'] = data_flag[windSpeed_cols].mean(axis=1, skipna=False)
data_flag['power_avg'] = data_flag[power_cols].mean(axis=1, skipna=False)
print(data_flag['power_avg'].describe())


# Draw power curve with average wind farm values
powerCurve(data_norm, 15)
plt.title(r"Anomalous = $\bf{False}$")

powerCurve(data_flag, 15)
plt.title(r"Anomalous = $\bf{True}$")



# Histograms of clean data
plt.figure()
plt.hist(data_flags['power_avg'].dropna(), edgecolor='k', label='unflagged + anomalous', alpha=0.8)
plt.hist(data_test['power_avg'].dropna(), edgecolor='k', label='unflagged', alpha=0.8)
plt.xlabel('normalised power [p.u.]'); plt.ylabel('count')
plt.title('Wind farm power distribution')
plt.legend(); plt.tight_layout()


# Boxplots of clean data
boxes = [data_test['power_avg'].dropna(), data_flags['power_avg'].dropna()]
boxprops = dict(linestyle='-', linewidth=2.5, color='k')
medianprops = dict(linewidth=2.0, color='b')
meanpointprops = dict(marker='D', markeredgecolor='black', markerfacecolor='b')
plt.figure()
plt.boxplot(boxes, showmeans=True, vert=False, 
            boxprops=boxprops, medianprops=medianprops, meanprops=meanpointprops)
plt.yticks([1,2], ['unflagged', 'unflagged + \nanomalous  '], fontsize=16, ha='right')
plt.xlabel('normalised power [p.u.]'); plt.title('Wind farm power distribution')
plt.tight_layout()



