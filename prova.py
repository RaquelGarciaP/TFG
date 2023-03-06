import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import collections


df = pd.read_csv('./NewLibrary/file_11600')
# df = pd.read_csv('./OldLibrary/lte12000-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', names=['wl', 'flux'])
standard_wl = pd.read_csv('./NewLibrary/standard_wl')

'''
min = 5199.9
max = 9600.1
'''
# mask = (df['wl'] >= min) & (df['wl'] <= max)
'''mask = (df['wl'] >= 6500.0)  # & (df['wl'] <= max)
df = df[mask]'''

min = df['wl'].iloc[0]
max = df['wl'].iloc[-1]
position = len(df)/2
print(len(df), position)
middle = df['wl'].iloc[81200]
mu = middle  # 7065.010522549267  # min + (max - min) / 2.0

print(min, max)
print(mu)

# sigma = 0.04
# sigma of the gaussian
'''R = 94600.0
ct = 1.0 / (2.35482 * R)  # delta_lambda = lambda/R = FWHM = 2*sqrt(2*ln2)*sigma = 2.35482 * sigma
sigma = ct * df['wl']'''

c = 299792458.0  # light velocity (m/s)
vel_rotation = 100.0
ct = 0.00001  # vel_rotation / (2.35482 * c)
wl = df['wl'].copy()
sigma = ct * wl

copia = df['flux'].copy()

gauss_norm = collections.deque()

print('calculating gaussian')
for i in range(len(df)):
    gauss_norm.append((standard_wl['delta wl'].iloc[i] / (math.sqrt(2.0 * math.pi) * sigma.iloc[i])) * np.exp(-((float(df['wl'].iloc[i]) - mu) / float(sigma.iloc[i])) ** 2 / float(2)))


delta_wl_phoenix = 0.01

gauss_norm = list(gauss_norm)
# gauss_norm = [x * standard_wl['delta wl'] for x in gauss_norm]
'''for i in range(len(gauss_norm)):
    # gauss_norm[i] = gauss_norm[i] * delta_wl_phoenix
    gauss_norm[i] = gauss_norm[i] * standard_wl['delta wl'].iloc[i]'''

gaussian = [x * 10000000000000000 for x in gauss_norm]
'''plt.plot(df['wl'], gaussian)
plt.show()'''

print('doing convolution')
df['flux'] = sp.signal.fftconvolve(copia, gauss_norm, mode='same')
print(df)

print('checking integral')
integral_i = 0.0
integral_f = 0.0

for i in range(len(df)):
    integral_i += standard_wl['delta wl'].iloc[i] * copia.iloc[i]
    # integral_i += delta_wl_phoenix * copia.iloc[i]

for i in range(len(df)):
    integral_f += standard_wl['delta wl'].iloc[i] * df['flux'].iloc[i]
    # integral_f += delta_wl_phoenix * df['flux'].iloc[i]

diff = abs(integral_i - integral_f)
print('Integral initial state: ', integral_i)
print('Integral final state: ', integral_f)
print('Difference: ', diff, '   Difference / initial flux: ', diff / integral_i)

print('doing plot')
fig, ax = plt.subplots()

l1, = ax.plot(df['wl'], copia)
l2, = ax.plot(df['wl'], df['flux'])
l3, = ax.plot(df['wl'], gaussian)

ax.legend((l1, l2, l3), ('initial flux', 'convolution norm', 'gaussian'), loc='upper right', shadow=False)
ax.set_xlabel('Wavelength (A)')
ax.set_ylabel('Flux')
ax.set_title('Convolution check')
plt.show()





