import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import collections
import time


# x = np.linspace(1.0,20.0, num=100)
# wl = pd.read_csv('./NewLibrary/standard_wl')
df = pd.read_csv('./OldLibrary/lte12000-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', names=['wl', 'flux'])

min = 5200.0  # df['wl'].iloc[0]
max = 9600.0  # df['wl'].iloc[-1]
mu = min + (max - min) / float(2)

mask = (df['wl'] >= min) & (df['wl'] <= max)
df = df[mask]

sigma = 0.85

gaussian = collections.deque()
gauss_norm = collections.deque()

for i in range(len(df)):
    gaussian.append(np.exp(-((float(df['wl'].iloc[i]) - mu) / float(sigma)) ** 2 / float(2)))
    gauss_norm.append((1.0 / (math.sqrt(2.0 * math.pi) * sigma)) * np.exp(-((float(df['wl'].iloc[i]) - mu) / float(sigma)) ** 2 / float(2)))

'''area1 = 0.0
for i in range(len(wl)):
    area1 += wl['delta wl'].iloc[i] * gaussian[i]

area2 = 0.0
for i in range(len(wl)):
    area2 += wl['delta wl'].iloc[i] * gauss_norm[i]

print(area1, area2)'''

'''inici_np = time.time()
convolution_np = np.convolve(df['flux'], gauss_norm, mode='same')
final_np = time.time()
print('np', final_np-inici_np)'''

# inici_sp = time.time()
conv_gauss = sp.signal.fftconvolve(df['flux'], gaussian, mode='same')
conv_norm = sp.signal.fftconvolve(df['flux'], gauss_norm, mode='same')
# final_sp = time.time()
# print('sp', final_sp-inici_sp)

fig, ax = plt.subplots()

l1, = ax.plot(df['wl'], df['flux'])
l2, = ax.plot(df['wl'], conv_gauss)
l3, = ax.plot(df['wl'], conv_norm)

ax.legend((l1, l2, l3), ('initial flux', 'convolution gauss', 'convolution norm'), loc='upper right', shadow=False)
ax.set_xlabel('Wavelength (A)')
ax.set_ylabel('Flux')
ax.set_title('Convolution check')
plt.show()

# plt.plot(df['wl'], df['flux'])
# plt.show()









