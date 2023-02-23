import pandas as pd
import collections


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
df = pd.DataFrame(dic)

# save to file
df.to_csv('./NewLibrary/standard_wl', index=False)



