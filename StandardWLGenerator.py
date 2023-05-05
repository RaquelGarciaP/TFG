import pandas as pd
import collections
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt


# ************** OWN STANDARD WAVELENGTH **************
'''
# create the collection that will contain the wavelength array
standard_wl = collections.deque()

# create the collection that will contain the delta_wavelength array (separation between each wl)
delta_wl = collections.deque()

# wavelength range (visible: 5200 A - 9600 A;  where [A]=Angstrom)
initial_wl = 5200.0
final_wl = 9600.0

# CARMENES sampling parameters
R = 94600.0  # resolution power
resol = 2.8  # pixels per resolution element

# loop to calculate each lambda (i) an delta_lambda (i / resol * R)
i = initial_wl
standard_wl.append(initial_wl)  # save the first wl (before modification inside the loop)
delta_wl.append(i / (resol * R))  # save the first delta_wl (before modification inside the loop)
while i <= final_wl:
    i = i + i / (resol * R)
    # fill the wl array
    standard_wl.append(i)
    delta_wl.append(i / (resol * R))

# convert the collection to list
list_wl = list(standard_wl)
list_delta = list(delta_wl)
# create a dictionary with the data
dic = {'wl': list_wl, 'delta wl': delta_wl}
# convert the list to pandas data frame
df = pd.DataFrame(dic)'''

# ************** CARMENES WAVELENGTH **************

hdul = fits.open('car-20160520T03h10m13s-sci-gtoc-vis_A.fits')

initial_order = 2
final_order = 54

total_grid = hdul['WAVE'].data[initial_order]

for i in range(final_order-2):
    total_grid = np.concatenate([total_grid, hdul['WAVE'].data[i+initial_order+1]])
    # print(i+initial_order+1)
    # print(i)

# print(total_grid)

delta_wl = np.empty(len(total_grid))
for i in range(len(total_grid)):
    if i + 1 == len(total_grid):
        print('he entrat aqui!!')
        delta_wl[i] = delta_wl[i-1]
    else:
        delta_wl[i] = total_grid[i+1] - total_grid[i]
    
print(np.amin(delta_wl))

# create a dictionary with the data
dic = {'wl': total_grid, 'delta wl': delta_wl}
# convert the list to pandas data frame
df = pd.DataFrame(dic)

# print(df)

lin = np.linspace(1, 100000, num=len(total_grid))
plt.plot(lin, dic['delta wl'], 'o')
plt.show()

# save to file
# df.to_csv('./NewLibrary/standard_wl', index=False)



