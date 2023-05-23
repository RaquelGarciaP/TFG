from astropy.io import fits
# from importlib.metadata import packages_distributions
# import importlib.metadata
import matplotlib.pyplot as plt
import pandas as pd
import sys
import getopt
import numpy as np
import os


hdul = fits.open('./CARMENES_data/car-20160520T03h10m13s-sci-gtoc-vis_A.fits')
hdul2 = fits.open('./CombinedSpectra/params_R21_is_zero/car-20160520T03h10m13s-sci-gtoc-vis_A.fits')
# hdul.info()
# hdul2.info()
# print(hdul[0].header['HIERARCH CARACAL BERV'])
# print(hdul['SPEC'].data[11])

order = 35

'''plt.plot(hdul['WAVE'].data[order], hdul['SPEC'].data[order])
plt.show()

plt.plot(hdul['WAVE'].data[order], hdul['SPEC'].data[order])
plt.show()'''

fig, ax = plt.subplots()

l1, = ax.plot(hdul['WAVE'].data[order], hdul['SPEC'].data[order])
l3, = ax.plot(hdul2['WAVE'].data[order], hdul2['SPEC'].data[order]/50)

ax.legend((l1, l3), ('carmenes', 'synthetic'), loc='upper right', shadow=False)
ax.set_xlabel('Wavelength (A)')
ax.set_ylabel('Flux')
ax.set_title('carmenes vs synthetic')
# ax.grid(True)
plt.show()


hdul.close()
hdul2.close()

# order = 44

# plt.plot(hdul['WAVE'].data[order], hdul['SPEC'].data[order])
# plt.show()

'''standard_wl = pd.read_csv('./NewLibrary/standard_wl')
mask = (standard_wl['wl'] >= hdul['WAVE'].data[order][0]) & (standard_wl['wl'] <= hdul['WAVE'].data[order][4095])
standard_wl = standard_wl[mask]

print('\n')
print(hdul['WAVE'].data[order])
print(standard_wl['wl'].to_numpy())

print('\n')
print(len(hdul['WAVE'].data[2]))
print(len(standard_wl))'''

'''print('\n')
CARMENES_data = fits.getdata('car-20160520T03h10m13s-sci-gtoc-vis_A.fits', header=True)
print(CARMENES_data[2].data[2])
CARMENES_data.info()
'''
# hdul.close()


'''total_grid = hdul['SPEC'].data[0]
# print(total_grid)

for i in range(60):
    total_grid = np.concatenate([total_grid, hdul['SPEC'].data[i+1]])

print(total_grid)'''
# print(type(total_grid))
# print(len(total_grid))

# np.savetxt('CARMENES_file1.csv', total_grid, delimiter=',')

'''hdul = fits.open('car-20201023T19h36m49s-sci-gtoc-vis_A.fits')
# hdul.info()
print('\n')
# print(hdul['WAVE'].header)
# print(hdul['WAVE'].data[0])
# print(hdul['WAVE'].data[60])
# print('\n')


total_grid2 = hdul['SPEC'].data[0]
# print(total_grid2)

for i in range(60):
    total_grid2 = np.concatenate([total_grid2, hdul['SPEC'].data[i+1]])

print(total_grid2)
# print(type(total_grid2))
# print(len(total_grid2))

x = np.linspace(0.0, 100, 249856)

plt.plot(x, total_grid)
plt.plot(x, total_grid2)
plt.show()'''


'''df = pd.read_pickle('./CombinedSpectra/output/RASSINE_not_normalized_spectra.p')
wave = pd.read_csv('./NewLibrary/standard_wl')
# print(df)

normalized_flux = df['flux'] / df['output']['continuum_linear']
# normalized_flux = df['flux_time_0']

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
