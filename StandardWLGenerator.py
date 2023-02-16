import pandas as pd
import collections


# create the collection that will contain the wavelength array
standard_wl = collections.deque()

# wavelength range (visible: 5200 A - 9600 A;  where [A]=Angstrom)
initial_wl = 5199.0
final_wl = 9601.0

# CARMENES sampling parameters
R = 94600.0  # resolution power
resol = 2.3

# loop to calculate each lambda (i) an delta_lambda (i / resol * R)
i = initial_wl
while i <= final_wl:
    i = i + i / (resol * R)
    # fill the wl array
    standard_wl.append(i)

# convert the collection to list
list_data = list(standard_wl)
# convert the list to pandas data frame
df = pd.DataFrame(list_data, columns=['wl'])

# save to file
df.to_csv('./NewLibrary/standard_wl', index=False)



