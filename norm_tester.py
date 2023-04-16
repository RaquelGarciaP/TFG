import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
from specutils.spectra import Spectrum1D, SpectralRegion
from specutils.fitting import fit_generic_continuum
from specutils.manipulation import extract_region
import warnings
from astropy import units as u
from astropy.io import fits
import rassine

'''
df_all = pd.read_csv('./CombinedSpectra/test_file_20t.csv')
df = pd.DataFrame()
df['wl'] = df_all['wl_time_0'].copy()
df['flux'] = df_all['flux_time_0'].copy()

data = df.values
hdu = fits.PrimaryHDU(data=data)
hdu.header.append(('TTYPE1', 'wave'))
hdu.header.append(('TTYPE2', 'flux'))
hdu.writeto('archivo.fits', overwrite=True)
'''
hdul = fits.open('archivo.fits')
hdul.info()
print(hdul[0].header)

'''
spectrum = Spectrum1D(flux*u.Jy, wl*u.Angstrom)

norm_flux = fit_generic_continuum(spectrum)  # sp.ndimage.median_filter(flux, size=101)
# norm_flux = sp.stats.sigmaclip(flux)
print(len(norm_flux))'''


'''fig, ax = plt.subplots()

l1, = ax.plot(df['wl'], df['flux'])
l2, = ax.plot(df['wl'], norm_flux)

ax.legend((l1, l2), ('flux', 'median filter'), loc='upper right', shadow=False)
ax.set_xlabel('Wavelength (A)')
ax.set_ylabel('Flux')
ax.set_title('Continuum Fitting')
ax.grid(True)
plt.show()'''


'''from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from ContinuumNormalization import ContinuumNormalization

# Create a sample DataFrame
df = pd.DataFrame({
    'A': [10, 20, 30, 40],
    'B': [5, 15, 25, 35],
    'C': [1, 2, 3, 4]
})

# Create a MinMaxScaler object
scaler = MinMaxScaler()

# Normalize the DataFrame
df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# Print the normalized DataFrame
print(df_normalized)'''


'''df = pd.read_csv('./CombinedSpectra/test_file.csv')
df_time0 = pd.DataFrame()
df_time0['wl'] = df['wl_time_0'].copy()
df_time0['flux'] = df['flux_time_0'].copy()

test = ContinuumNormalization(df_time0)
'''

