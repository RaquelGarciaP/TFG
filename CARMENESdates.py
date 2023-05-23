import numpy as np
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
import os


FILENAME_arr = os.listdir('./CARMENES_data')
print(FILENAME_arr)

BJD_arr = np.empty(len(FILENAME_arr))
BERV_arr = np.empty(len(FILENAME_arr))

for i in range(len(FILENAME_arr)):
    file_path = './CARMENES_data/' + FILENAME_arr[i]
    hdul = fits.open(file_path)
    BJD_arr[i] = hdul[0].header['HIERARCH CARACAL BJD'] - 57000
    BERV_arr[i] = hdul[0].header['HIERARCH CARACAL BERV'] * 1000  # passem a m/s
    hdul.close()


df = pd.DataFrame({'FILENAME': FILENAME_arr, 'BJD': BJD_arr, 'BERV': BERV_arr})
df.to_csv('./CARMENES_data/info_observations.csv', index=False)


# df_read = pd.read_csv('./CARMENES_data/info_observations.csv')
# print(type(df_read['FILENAME'].iloc[0]))



'''df_read = pd.read_csv('./CARMENES_data/info_observations.csv')

dates_arr = df_read['BJD'].to_numpy()
np.save('./NewLibrary/CARMENESdates', dates_arr)'''





