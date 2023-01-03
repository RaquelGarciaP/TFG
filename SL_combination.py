import numpy as np
import pandas as pd


class SL_combination:
    """Spectral Lines combination class"""

    def __init__(self, file1: str, file2: str):

        # we read both files with the library pandas
        self.__file1 = pd.read_csv(file1)
        self.__file2 = pd.read_csv(file2)

        # we obtain the number of rows (number of data) of each file:
        self.__rows1 = len(self.__file1)
        self.__rows2 = len(self.__file2)

        # we create the arrays where the wave length and the flux of the 1st file will be saved
        self.__wl1 = np.empty(self.__rows1)
        self.__flux1 = np.empty(self.__rows1)

        # we create the arrays where the wave length and the flux of the 2nd file will be saved
        self.__wl2 = np.empty(self.__rows2)
        self.__flux2 = np.empty(self.__rows2)

        # we fill the initial wl and flux of the 1st file
        self.__fill_wl(self.__wl1, self.__file1)
        self.__fill_flux(self.__flux1, self.__file1)

        # we fill the initial wl and flux of the 2nd file
        self.__fill_wl(self.__wl2, self.__file2)
        self.__fill_flux(self.__flux2, self.__file2)

    def __fill_wl(self, array, file):
        # we save the initial wave length in a numpy array:
        for i in range(len(file)):
            array[i] = file.loc[i].iat[0]
            # loc[i] = i-est element of the column; iat[0] = zero column (where the wave length is)

    def __fill_flux(self, array, file):
        # we save the initial flux in a numpy array:
        for i in range(len(file)):
            array[i] = file.loc[i].iat[1]

    def combine_files(self):

        if self.__rows1 == self.__rows2:
            # we create an array where we will save the final sum
            final_sum = np.empty(self.__rows1)
            # loop to do the sum
            for i in range(self.__rows1):
                if self.__wl1[i] == self.__wl2[i]:
                    final_sum[i] = self.__flux1[i] + self.__flux2[i]
                else:
                    final_sum[i] = 0.0

            return final_sum

        else:
            # we select the minimum number of rows between both files
            number_iterations = min(self.__rows1, self.__rows2)
            # we create an array where we will save the final sum
            final_sum = np.empty(number_iterations)
            # loop to do the sum
            for i in range(number_iterations):
                if self.__wl1[i] == self.__wl2[i]:
                    final_sum[i] = self.__flux1[i] + self.__flux2[i]
                else:
                    final_sum[i] = 0.0

            # notice that if the files do not have the same size, we only combine them while they coincide

            return final_sum

    def do_plot(self): ...

    def save_to_file(self): ...



