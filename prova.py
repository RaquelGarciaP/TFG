import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import collections
import time


df = pd.read_csv('./OldLibrary/lte12000-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', names=['wl', 'flux'])

min = 5198.9  # df['wl'].iloc[0]
max = 9601.1  # df['wl'].iloc[-1]
mu = min + (max - min) / 2.0

mask = (df['wl'] >= min) & (df['wl'] <= max)
df = df[mask]

# sigma = 0.04
# sigma of the gaussian
R = 94600.0
ct = 1.0 / (2.35482 * R)  # delta_lambda = lambda/R = FWHM = 2*sqrt(2*ln2)*sigma = 2.35482 * sigma
sigma = ct * df['wl']

copia = df['flux'].copy()

gauss_norm = collections.deque()

for i in range(len(df)):
    gauss_norm.append((1.0 / (math.sqrt(2.0 * math.pi) * sigma.iloc[i])) * np.exp(-((float(df['wl'].iloc[i]) - mu) / float(sigma.iloc[i])) ** 2 / float(2)))


delta_wl_phoenix = 0.01

gauss_norm = list(gauss_norm)
gauss_norm = [x * delta_wl_phoenix for x in gauss_norm]

df['flux'] = sp.signal.fftconvolve(copia, gauss_norm, mode='same')

integral_i = 0.0
integral_f = 0.0

for i in range(len(df)):
    integral_i += delta_wl_phoenix * copia.iloc[i]

for i in range(len(df)):
    integral_f += delta_wl_phoenix * df['flux'].iloc[i]

diff = abs(integral_i - integral_f)
print('Integral initial state: ', integral_i)
print('Integral final state: ', integral_f)
print('Difference: ', diff, '   Difference / initial flux: ', diff / integral_i)

fig, ax = plt.subplots()

l1, = ax.plot(df['wl'], copia)
l2, = ax.plot(df['wl'], df['flux'])

ax.legend((l1, l2), ('initial flux', 'convolution norm'), loc='upper right', shadow=False)
ax.set_xlabel('Wavelength (A)')
ax.set_ylabel('Flux')
ax.set_title('Convolution check')
plt.show()





