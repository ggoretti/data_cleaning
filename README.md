# Cleaning wind turbine data

This repository includes the scripts developed for cleaning wind turbine data.

An example where the functions are applied is also included.

## Use this code

### Function
The function that performs turbine data cleaning is **`clean_turbine`**.

### Assumptions
Data Quality:
* _consistency_: data are presented in the same format (for example, measurements coming from different SCADA systems)
* _uniformity_: measures are specified using the same units across different systems (for example, wind speed in m/s, timestamps with same UTC offset, ...)

Variables (for each turbine):
* wind speed [m/s]
* power (_normalised_ by rated capacity) [p.u.]

### Data format
* Data: `pandas.DataFrame`
* Columns:
  - index: unique for all columns (`pandas.DatetimeIndex`)
  - wind speed = `['windSpeed_wt01', 'windSpeed_wt02', ..., 'windSpeed_wtNN']`
  - power = `['power_wt01', 'power_wt02', ..., 'power_wtNN']`
* Packages required: `pandas`, `numpy`, `matplotlib`

