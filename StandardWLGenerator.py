import pandas as pd
import collections

standard_wl = collections.deque()

# wavelength range (visible: 5200 A - 9600 A;  where [A]=Angstrom)
initial_wl = 5199
final_wl = 5203

R = 94600.0
resol = 2.3

i = initial_wl
while i <= final_wl:
    i = i + i / (resol * R)
    print(i)
    standard_wl.append(i)

print(standard_wl)
df = pd.DataFrame(standard_wl)

