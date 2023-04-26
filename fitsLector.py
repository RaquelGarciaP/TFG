from astropy.io import fits
# from importlib.metadata import packages_distributions
# import importlib.metadata
import matplotlib.pyplot as plt
import pandas as pd
import sys
import getopt


hdul = fits.open('car-20160520T03h10m13s-sci-gtoc-vis_A.fits')
hdul.info()
print('\n')
print(hdul['WAVE'].header)
print(hdul['WAVE'].data[60])
print(hdul['WAVE'].data[0])

'''
df = pd.read_pickle('./CombinedSpectra/output/RASSINE_not_normalized_spectra.p')
# wave = pd.read_csv('./NewLibrary/standard_wl')
# print(df)

# normalized_flux = df['flux'] / df['output']['continuum_linear']
normalized_flux = df['flux_time_0']

plt.plot(wave['wl'], normalized_flux)
plt.grid(True)
plt.show()

fig, ax = plt.subplots()

l1, = ax.plot(df['wave'], df['flux'])
# l2, = ax.plot(df['wave'], df['output']['continuum_cubic'])
l3, = ax.plot(df['wave'], df['output']['continuum_linear'])

ax.legend((l1, l3), ('flux', 'continuum linear'), loc='upper right', shadow=False)
ax.set_xlabel('Wavelength (A)')
ax.set_ylabel('Flux')
ax.set_title('Continuum Fitting')
ax.grid(True)
plt.show()
'''
