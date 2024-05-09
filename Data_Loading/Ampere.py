from xarray import load_dataset
import numpy as np

def load_ampere(file):
    """
    Loads AMPERE data from a NetCDF file using xarray.

    Parameters:
        file (str): Path to the nc file containing AMPERE data.

    Returns:
        xarray.Dataset: AMPERE data loaded as an xarray dataset.

    Raises:
        UserWarning: If the provided file is empty and contains no AMPERE data.

    """
    # Load dataset from the given file
    AMP_data = load_dataset(file)
    
    # Check if the dataset is empty
    if not len(AMP_data.nRec):
        raise UserWarning('File empty no AMPERE data')
    
    # Rename dimension from 'nRec' to 'mid_point'
    AMP_data = AMP_data.rename_dims({'nRec':'mid_point'})
    
    # Assign new coordinates based on year, day of year (doy), and time
    AMP_data = AMP_data.assign_coords(mid_point=AMP_data.year.astype(str).astype('datetime64[Y]') + \
                                    (AMP_data.doy - 1).astype('timedelta64[D]') + \
                                    np.round((AMP_data.time * 60 * 60 + 60).values.astype('timedelta64[s]'). \
                                    astype(float) / 60).astype('timedelta64[m]'))
    
    # Rename variables 'geo_cLat_deg' to 'glat' and 'geo_lon_deg' to 'glon'
    AMP_data = AMP_data.rename_vars({'geo_cLat_deg': 'glat', 'geo_lon_deg': 'glon'})
    
    # Convert 'glat' from colat to lat
    AMP_data['glat'] = 90 - AMP_data['glat']
    
    return AMP_data