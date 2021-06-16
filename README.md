# Cleaning wind turbine data

This repository includes the scripts developed for cleaning wind turbine data, when wind speed and power values for each turbine in the wind farm are available.

## Use this code

### Function
The function that performs turbine data cleaning is **`clean_turbine`**.

An example of the application of the _clean_turbine_ function is presented in `example.py`.
The function `powerCurve.py` is also included, which draws the "wind farm" power curve using the average turbine values, namely wind speed and power.



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

