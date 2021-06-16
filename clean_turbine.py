# -*- coding: utf-8 -*-

def clean_turbine(data_raw, wtn, ws_cut_in, ws_rated, ws_cut_out, 
                  k_up=1.5, k_low=1.5, anomalous=False):
    '''
    Cleans wind turbine data.
    
    Variables
    ----------
    data_raw : DataFrame
        Raw data to be cleaned.
    wtn : int
        Number of wind turbines.
    ws_cut_in : float
        Cut-in wind speed in m/s.
    ws_rated : float
        Rated wind speed in m/s.
    ws_cut_out : float
        Cut-out wind speed in m/s.
    k_up : float, default=1.5
        Multiplier of IQR to define upper threshold for outlier detection.
    k_low : float, default=1.5
        Multiplier of IQR to define lower threshold for outlier detection.
    anomalous : bool, default False
        If True, anomalous (flagged) periods are kept in the data set.
    
    Returns
    ----------
    data : pandas.DataFrame
        Cleaned data.
    
    Notes
    -----
    Wind speed values are in m/s.
    Power values are normalised by rated power.

    '''
    
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

    
    # = = = = = DATA CLEANING = = = = = 
    data = data_raw.copy()


    # = = = = = COMPLETENESS of data = = = = =
    print("\n######################### MISSING DATA ######################### \n")
    print("- - - - - Wind speed missing values - - - - -")
    for wt,ws in zip(range(1, wtn+1), windSpeed_cols):
        print("Turbine " + str(wt).zfill(2) + ": " +
              str(data[ws].isnull().sum()) + " (" +
              str(round(data[ws].isnull().sum()/float(len(data[ws]))*100, 1)) + "%)")
          
    print("\n - - - - - Power missing values - - - - -")
    for wt,pw in zip(range(1, wtn+1), power_cols):
        print("Turbine " + str(wt).zfill(2) + ": " +
              str(data[pw].isnull().sum()) + " (" +
              str(round(data[pw].isnull().sum()/float(len(data[pw]))*100, 1)) + "%)")
    print("\n###############################################################")

    
    # = = = = = VALIDITY of data = = = = =
    # - - - Univariate extreme values - - -
    # Wind speed
    for ws in windSpeed_cols:
        data[ws].where(
            (data[ws]>=0) & (data[ws]<40)
            )
    
    # Power
    for pw in power_cols:
        data[pw].where(
            (data[pw]>=-0.02) & (data[pw]<1.01)
            )
    
    
    # - - - Bivariate extreme values - - -
    # Rules: remove erroneous data, flag anomalous data.
    
    # Create a flag column for each turbine and set initial value to 0.
    # When the data is anomalous, the flag value is set > 0.
    flag_cols = ['flag_wt' + str(wt).zfill(2) for wt in range(1,wtn+1)]
    for fl in flag_cols:
        data[fl] = 0
    
    # 1. Remove instances of high power output for wind speed in [0, ws_cut_in]
    for ws,pw in zip(windSpeed_cols, power_cols):
        data[pw] = data[pw].mask(
            (data[ws] >= 0) & (data[ws] < ws_cut_in) &
            (data[pw] > 0.04)
            )

    # 2. Remove instances of non-zero power for wind speed > ws_cut_out + 2
    for ws,pw in zip(windSpeed_cols, power_cols):
        data[pw] = data[pw].mask(
            (data[ws] >= ws_cut_in+2) &
            (data[pw] > 0)
            )

    # 3. Flag instances of zero power output for wind speed in [ws_cut_in+2,
    #    ws_cut_out-2]
    # Create a list of "temporary" columns for partially-clean power values
    power_cols_tmp = ['power_wt' + str(wt).zfill(2) + "_tmp" for wt in range(1,wtn+1)]
    for ws,pw,fl,pw_tmp in zip(windSpeed_cols, power_cols, flag_cols, power_cols_tmp):
        data[fl] = data[fl].mask(
            (data[ws] > ws_cut_in+2) & (data[ws] < ws_cut_out-2) & 
            (data[pw] < 0.005),
            data[fl]+1
            )
        data[pw_tmp] = data[pw].mask(data[fl] > 0)

    
    # 4. Flag instances of low power output (<99.5% of P_nom) for wind speed in 
    #    [ws_rated+2, ws_cut_out-2]
    for ws,pw,fl in zip(windSpeed_cols, power_cols, flag_cols):
        data[fl] = data[fl].mask(
            (data[ws] > ws_rated+2) & (data[ws] < ws_cut_out-2) &
            (data[pw] < 0.995),
            data[fl]+1
            )


    # 5. Remove instances of high power output for wind speed in [ws_cut_in+0.5, ws_rated]
    bin_width = 0.05  # [m/s]
    for ws,pw,fl,pw_tmp in zip(windSpeed_cols, power_cols, flag_cols, power_cols_tmp):
        # 5.1 Group by wind speed values, bin width = bin_width
        grouped = data.groupby(
            pd.cut(data[ws], np.arange(ws_cut_in+0.5, ws_rated, bin_width))
            )
        for key,df in grouped:
            # 5.2 Calculate outlier threshold (Q3 + 2.5*IQR) for each group
            q25, q75 = np.percentile(df[pw_tmp].dropna(), [25,75])
            iqr = q75 - q25
            thresh_up = q75 + k_up*iqr
        
            # 5.3 Remove instances where power is above the threshold
            data[pw] = data[pw].mask(
                (data[ws] > key.left) & (data[ws] <= key.right) &
                (data[pw] > thresh_up)
                )


    # 6. Flag instances of low power output for wind speed in [ws_cut_in+0.5, ws_rated+2.0]
    bin_width = 0.05  # [m/s]
    for ws,pw,fl,pw_tmp in zip(windSpeed_cols, power_cols, flag_cols, power_cols_tmp):
        # 6.1 Group by wind speed values, bin width=bin_width.
        grouped = data.groupby(
            pd.cut(data[ws], np.arange(ws_cut_in+0.5, ws_rated+2.0+bin_width, bin_width))
            )
        
        for key,df in grouped:
            # 6.2 Calculate outlier threshold (Q1 - 2.5*IQR) for each group
            q25, q75 = np.percentile(df[pw_tmp].dropna(), [25,75])
            iqr = q75 - q25
            thresh_low = q25 - k_low*iqr
    
            # 6.3 Flag instances where power output is below the threshold
            data[fl] = data[fl].mask(
                (data[ws] > key.left) & (data[ws] <= key.right) &
                (data[pw] < thresh_low),
                data[fl]+1
                )
    
    
    # If anomalous=True, keep "flagged" periods in the data set, otherwise 
    # remove them.
    if anomalous == True:
        return(data)
    else:
        for pw,fl in zip(power_cols, flag_cols):
            data[pw] = data[pw].mask(data[fl] > 0)
        return(data)
    
