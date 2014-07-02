"""
This example code illustrates how to access and visualize GESDISC_TRMM file in
Python.  If you have any questions, suggestions, comments  on this example,
please use the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to
see an  example of any other NASA HDF/HDF-EOS data product that is not 
listed in the HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo),
feel free to contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).
"""
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import numpy as np

def run(FILE_NAME):

    # Identify the HDF-EOS2 swath data file.
    DATAFIELD_NAME = 'binDIDHmean'
    
    dset = Dataset(FILE_NAME)
    data = dset.variables[DATAFIELD_NAME][:].astype(np.float64)
    
    # Retrieve the geolocation data.
    latitude = dset.variables['geolocation'][:,:,0]
    longitude = dset.variables['geolocation'][:,:,1]
    
    # Draw an equidistant cylindrical projection using the high resolution
    # coastline database.
    m = Basemap(projection='cyl', resolution='h',
                llcrnrlat=31, urcrnrlat = 36,
                llcrnrlon=122, urcrnrlon = 133)
    
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(31, 36))
    m.drawmeridians(np.arange(122, 133))
    
    # Render the image in the projected coordinate system.
    x, y = m(longitude, latitude)
    m.pcolormesh(x, y, data)
    m.colorbar()
    fig = plt.gcf()
    
    plt.title('{0}'.format(DATAFIELD_NAME))
    plt.show()
    
    pngfile = "{0}.{1}.png".format(os.path.basename(FILE_NAME[:-4]),
                                   DATAFIELD_NAME)
    fig.savefig(pngfile)

if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    hdffile = '1B21_CSI.990906.10217.KORA.6.HDF'
    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    run(hdffile)
    
