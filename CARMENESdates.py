import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import juliandate as jd
import datetime as dt


head = ['BJD', 'RVC', 'E_RVC', 'DRIFT', 'E_DRIFT', 'RV', 'E_RV', 'BERV', 'SADRIFT']
df = pd.read_csv('D:/raquel/Desktop/UNI/5e/TFG/observacions CARMENES/dates de mesura de CARMENES/J18356+329.rvc.csv', names=head)

# print(df['RVC'].mean())
# print(df['RV'].mean())

# plt.plot(df['BJD'], df['RVC'], 'o')
# plt.show()

# ************************* convert julian date to georgian date *************************
georgian_date = []
for i in range(len(df['BJD'])):
    georgian_date.append(jd.to_gregorian(df['BJD'].iloc[i]))  # year, month, day, hour, minute, second, fraction of sec?

print(georgian_date)

# ************************* list of file names (after SpectraCombiner) *************************
# CARMENES file name example: car-20160520T03h10m13s-sci-gtoc-vis_A.fits
'''file_names = []
# file_names = np.empty(len(georgian_date), dtype=str)
# file = open('file_names.txt', 'w')  # file where we save the file names
for i in range(len(georgian_date)):
    file_name_i = 'car-' + str(georgian_date[i][0]) + str(georgian_date[i][1]) + str(georgian_date[i][2]) + 'T' + \
                  str(georgian_date[i][3]) + 'h' + str(georgian_date[i][4]) + 'm' + str(georgian_date[i][5]) + 's' + \
                  '-sci-gtoc-vis_A.fits'
    # file.write(file_name_i+'\n')  # save into file
    file_names.append(file_name_i)  # we also save in a list to check the result in console
    # file_names[i] = file_name_i

array_names = np.array(file_names)
np.save('file_names', array_names)
print(array_names)'''

# loaded_names = np.load('./NewLibrary/file_names.npy')
# print(loaded_names[0])


'''with open('./NewLibrary/file_names.txt', 'r') as file:
    names = file.read()
print(names[2])'''


# ************************* array with time in seconds *************************
'''difference_in_seconds = np.empty(len(georgian_date))
difference_in_seconds[0] = 0.0
total_time = 0.0
for i in range(len(georgian_date)-1):
    a = dt.datetime(georgian_date[i][0], georgian_date[i][1], georgian_date[i][2], georgian_date[i][3], georgian_date[i][4], georgian_date[i][5])
    b = dt.datetime(georgian_date[i+1][0], georgian_date[i+1][1], georgian_date[i+1][2], georgian_date[i+1][3], georgian_date[i+1][4], georgian_date[i+1][5])
    total_time += (b - a).total_seconds()
    difference_in_seconds[i+1] = total_time  # (b-a).total_seconds()

print(difference_in_seconds)

plt.plot(difference_in_seconds, df['RVC'], 'o')
plt.show()

np.save('./NewLibrary/CARMENESdates', difference_in_seconds)
'''

# ************************* prova *************************
'''
a = dt.datetime(2016, 5, 20, 3, 30, 12)  # year, month, day, hour, minute, second
b = dt.datetime(2016, 6, 24, 1, 14, 6)

print((b-a).total_seconds())
'''



