# -*- coding: utf-8 -*-

def powerCurve(data, wtn):
    '''
    Plot wind farm power curve with average wind speed and power values.
    
    Variables
    ----------
    data : DataFrame
        Turbine wind speed and power data to plot.
    wtn : int
        Number of wind turbines.
    '''
    
    # List of wind speed column names
    windSpeed_cols = ['windSpeed_wt' + str(wt).zfill(2) for wt in range(1,wtn+1)]  # turbine wind speed
    
    # List of power column names
    power_cols = ['power_wt' + str(wt).zfill(2) for wt in range(1,wtn+1)]  # turbine active power
    
    # - - - Calculate wind farm statistics - - - 
    # Average wind speed
    data['windSpeed_avg'] = data[windSpeed_cols].mean(axis=1, skipna=False)
    # Standard deviation of wind speed
    data['windSpeed_std'] = data[windSpeed_cols].std(axis=1, skipna=False)
    # Average power output
    data['power_avg'] = data[power_cols].mean(axis=1, skipna=False)
    
    
    # Power curve
    plt.figure()
    plt.scatter(data['windSpeed_avg'], data['power_avg'], c=data['windSpeed_std'], cmap='plasma', edgecolor='k', alpha=0.9)
    # dots are coloured by wind speed standard deviation
    plt.xlabel('average wind speed [m/s]'); plt.ylabel('normalised average power [p.u.]')
    plt.title('Power curve - Raw data')
    plt.grid(ls='--', lw=0.5, c='grey')
    plt.tight_layout()
    plt.show()

