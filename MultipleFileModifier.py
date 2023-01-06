import numpy as np
import pandas as pd


class MultipleFileModifier:

    def __init__(self, T1, T2):
        self.__T1 = T1
        self.__T2 = T2

        # files that we want to read:
        self.__file_name_T1 = 'file_' + str(self.__T1) + '_' + str(self.__log_g) + '.csv'
        self.__file_name_T2 = 'file_' + str(self.__T2) + '_' + str(self.__log_g) + '.csv'

        # we read the file using the library pandas
        print('Reading the files')
        self.__df_T1 = pd.read_csv(self.__file_name_T1, names=['wl', 'flux'])
        self.__df_T2 = pd.read_csv(self.__file_name_T2, names=['wl', 'flux'])

        # we obtain the number of rows of our data (number of data we have per column); useful for iterations
        self.__nrows_T1 = len(self.__df_T1)
        self.__nrows_T2 = len(self.__df_T2)

        # save the initial data in the class variables for the wl and flux (will be MODIFIED)
        print('Saving the data in the class variables')
        self.__wl1 = self.__df_T1['wl']
        self.__flux1 = self.__df_T1['flux']
        self.__wl2 = self.__df_T2['wl']
        self.__flux2 = self.__df_T2['flux']

    def interpolate(self):
        # wl1 is the new axis for the wave length in both files
        # find in between which indices are the wl1 values with respect to wl2
        indices_left = np.searchsorted(self.__wl2, self.__wl1)
        indices_right = [x - 1 for x in indices_left]

        # copy of the array flux2
        initial_flux2 = self.__flux2

        # define a function for the linear interpolation
        def linear_interpolation(x, x0, y0, x1, y1):
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

        # loop to apply the linear interpolation to each element of flux2
        for i in range(self.__nrows_T1 - 2):
            self.__flux2 = linear_interpolation(self.__flux1[i+1], self.__wl2[indices_left[i]], initial_flux2[i], ...)  # ESTA MAL?




