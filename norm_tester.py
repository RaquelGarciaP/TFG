from astropy.io import fits
# from importlib.metadata import packages_distributions
# import importlib.metadata
import matplotlib.pyplot as plt
import pandas as pd
import sys
import getopt
import numpy as np


df = pd.read_pickle('./CombinedSpectra/cool_star/RASSINE_file_2300.p')
# wave = pd.read_csv('./NewLibrary/standard_wl')
# print(df)

normalized_flux = df['flux'] / df['output']['continuum_linear']
# normalized_flux = df['flux_time_0']

plt.plot(df['wave'], normalized_flux)
plt.title('Normalized flux')
plt.xlabel('Wavelength (A)')
plt.ylabel('Flux')
plt.grid(True)
plt.show()

'''fig, ax = plt.subplots()

l1, = ax.plot(df['wave'], df['flux'])
# l2, = ax.plot(df['wave'], df['output']['continuum_cubic'])
l3, = ax.plot(df['wave'], df['output']['continuum_linear'])

ax.legend((l1, l3), ('flux', 'continuum linear'), loc='upper right', shadow=False)
ax.set_xlabel('Wavelength (A)')
ax.set_ylabel('Flux')
ax.set_title('Continuum Fitting')
ax.grid(True)
plt.show()'''
