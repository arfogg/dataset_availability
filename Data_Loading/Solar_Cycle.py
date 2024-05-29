def load_sunspot_number():
    """
    Download and process daily sunspot number data.

    This function retrieves the daily sunspot number data from the SIDC (Solar Influences Data Analysis Center) 
    and processes it into a pandas DataFrame. The data includes the daily total sunspot number, daily standard 
    deviation, number of observations, and an indicator for definitive or provisional data.

    The function performs the following steps:
    1. Downloads the sunspot number data from the specified URL.
    2. Replaces missing values represented by -1 with NaN.
    3. Converts the 'Year', 'Month', and 'Day' columns into a single datetime index.
    4. Sets the datetime index and returns the relevant columns.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the following columns:
        - 'Daily_total_sunspot_number' : The daily total sunspot number.
        - 'Daily_standard_deviation' : The standard deviation of the daily sunspot number.
        - 'Number_of_observations' : The number of observations used to calculate the daily sunspot number.
        - 'Definitive_provisional_indicator' : An indicator whether the data is definitive or provisional.
    """
    import pandas as pd
    import numpy as np

    header_list = ['Year', 'Month', 'Day', 'Decimal_Year', 
                   'Daily_total_sunspot_number', 'Daily_standard_deviation', 
                   'Number_of_observations', 'Definitive_provisional_indicator']
    
    ss = pd.read_csv('http://www.sidc.be/silso/INFO/sndtotcsv.php', delimiter=';', names=header_list)
    ss = ss.replace(-1, np.nan)
    ss['Date'] = pd.to_datetime(ss[['Year', 'Month', 'Day']])
    ss.set_index('Date', inplace=True)
    
    return ss[['Daily_total_sunspot_number', 'Daily_standard_deviation', 
               'Number_of_observations', 'Definitive_provisional_indicator']]

def f107(stat_method='median'):
    """
    Download and process the Penticton radio flux data, resampling it based on the specified statistical method.

    Parameters:
    -----------
    stat_method : str, optional
        The statistical method to use for resampling the data. Options are:
        - 'min' : Minimum value for each day
        - 'mean' : Mean value for each day
        - 'median' : Median value for each day
        Default is 'median'.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the resampled Penticton radio flux data with two columns:
        - 'observed_solar_radio_flux' : Observed solar radio flux in solar flux units (SFU)
        - 'adjusted_solar_radio_flux' : Adjusted solar radio flux in solar flux units (SFU)

    Notes:
    ------
    - The function downloads the Penticton radio flux data from a specified URL.
    - The data is resampled to daily values using the specified statistical method.
    - The Julian date column is dropped from the data.
    - The downloaded file is removed after processing.

    Example:
    --------
    >>> f107('mean')
                         observed_solar_radio_flux  adjusted_solar_radio_flux
    1947-01-01                  75.3                         80.5
    1947-01-02                  74.8                         80.0
    ...

    """
    import requests
    import pandas as pd
    import numpy as np
    import os

    time_stamp = '2025-02-05T08:41:00.000Z'  # Arbitrary time, it automatically chooses the last available
    file_url_penticton = 'https://lasp.colorado.edu/lisird/latis/dap/penticton_radio_flux.csv?&time>=1947-01-01T00:00:00.000Z&time<=' + time_stamp
    filepath = './'
    filename_penticton = 'penticton_radio_flux.csv'
    filedata = requests.get(file_url_penticton)
    with open(filepath + filename_penticton, 'wb') as file:
        file.write(filedata.content)
    print('Penticton file downloaded...')

    # Read Penticton data
    f107new = pd.read_csv(filepath + filename_penticton, sep=',', parse_dates=True, index_col=0)
    f107new[f107new == 0] = np.nan

    # Convert Julian to datetime 
    time = np.array(f107new.index)
    epoch = pd.to_datetime(0, unit='s').to_julian_date()
    time = pd.to_datetime(time - epoch, unit='D')

    # Set datetime as index
    f107new = f107new.reset_index()
    f107new.set_index(time, inplace=True)

    # Resample the Penticton data set for one day
    f107new_min = f107new.resample('1D').min()
    f107new_mean = f107new.resample('1D').mean()
    f107new_median = f107new.resample('1D').median()

    # Drop the NaN's based on the chosen statistical method
    f107new = eval(f'f107new_{stat_method}.dropna()')

    # Drop Julian date column 
    f107new_median = f107new_median.drop(columns=['time (Julian Date)'], axis=1)

    # Extract the columns of interest
    f107observed_flux = f107new_median[f107new_median.keys()[0]].values
    f107adjusted_flux = f107new_median[f107new_median.keys()[1]].values

    # Create a pandas DataFrame with the columns of interest
    f107Penticton = pd.DataFrame(index=f107new.index, data={
        'observed_solar_radio_flux': f107new['observed_flux (solar flux unit (SFU))'].values,
        'adjusted_solar_radio_flux': f107new['adjusted_flux (solar flux unit (SFU))'].values
    })

    os.remove(filepath + filename_penticton)
    return f107Penticton
