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
        # we save the wl of the first file as the new 'x' axis
        self.__wl = self.__df_T1['wl']
        # the flux os the 1st file remains ct because has the same 'x'
        self.__flux1 = self.__df_T1['flux']
        # we initialize the class variable of the flux of the 2nd file. In this we'll save the data after
        # the interpolation (the 'x' axis changes -> interpolation to find the corresponding values for the new 'x')
        self.__flux2 = None

        # we create the class variable that will contain the flux after the sum of both files
        self.__combined_flux = None

    def interpolate(self):  # todo: potser aixo es pot fer al inicialitzar la classe directament
        # we do the interpolation and obtain the values for flux2 in the new axis of 'x'
        # (documentació de numpy explica que passa als extrems)
        self.__flux2 = np.interp(self.__wl, self.__df_T2['wl'], self.__df_T2['flux'])

    def sum(self):
        # we sum point to point each value of both fluxes using the 'map' function and converting the result to
        # a pandas 'Series' (easier to work with using the library pandas)
        self.__combined_flux = pd.Series(map(lambda x, y: x + y, self.__flux1, self.__flux2))





