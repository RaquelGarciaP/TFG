import numpy as np
import pandas as pd
import scipy as sp
import math
import matplotlib.pyplot as plt


class DopplerShift_and_Convolution:

    def __init__(self, T_eff, log_g):

        self.__T_eff = T_eff
        self.__log_g = log_g

        # file that we want to read:
        self.__initial_spectral_line = 'file_'+str(self.__T_eff)+'_'+str(self.__log_g)+'.csv'

        # we read the file using the library pandas
        print('Reading the file')
        self.__read_initial_spectral_line = pd.read_csv(self.__initial_spectral_line)

        # we obtain the number of rows of our data (number of data we have per column); useful for iterations
        self.__number_rows = len(self.__read_initial_spectral_line)

        # we create empty np.arrays where the data (wave_length and flux) will be saved:
        # VERY IMPORTANT: these arrays will be MODIFIED (we rewrite them when a modification is made)
        print('Creating the arrays that will contain the wave length and the flux')
        self.__wave_length = np.empty(self.__number_rows)  # wave length -> it is MODIFIED after the Doppler shift
        self.__flux = np.empty(self.__number_rows)  # flux -> it is MODIFIED after the convolution

        # we save each initial wave length (the ones in the file) rewriting the created numpy array:
        self.__fill_wl()
        # we save the initial flux (the one in the file) rewriting the created numpy array:
        self.__fill_flux()

    def __fill_wl(self):
        print('Saving the wave length in an array')
        # we save the initial wave lengths (the ones in the file) in the wave_length numpy array:
        for i in range(self.__number_rows):
            self.__wave_length[i] = self.__read_initial_spectral_line.loc[i].iat[0]
            # loc[i] = i-est element of the column; iat[0] = zero column (where the wave length is)
            # equivalent to wave_length.loc[0].at['wave_length'] where 'wave_length' is the name of the column

    def __fill_flux(self):
        print('Saving the flux in an array')
        # we save the initial flux (from the file) in the flux numpy array:
        for i in range(self.__number_rows):
            self.__flux[i] = self.__read_initial_spectral_line.loc[i].iat[1]

    def doppler_shift(self, vr_divided_c):  # vr_divided_c = radial_velocity/c (c: speed of light)
        print('Applying Doppler Shift')
        # we create a copy of the wave length array (called initial_data bc it's the data b4 this modification):
        initial_data1 = self.__wave_length
        # loop to apply the Doppler shift:
        for i in range(self.__number_rows):
            self.__wave_length[i] = (1 + vr_divided_c) * initial_data1[i]

    def convolution(self, sigma):
        print('Applying Convolution')
        # we create a copy of the flux array (called initial_data2 bc it's the data b4 this modification):
        initial_data2 = self.__flux
        # we create the array that will contain the gaussian:
        gaussian  = np.empty(self.__number_rows)

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.__wave_length[0]  # minimum wave length
        max_wl = self.__wave_length[-1]  # maximum wave length
        center_gaussian = min_wl + (max_wl - min_wl) / float(2)

        # loop to calculate the gaussian:
        for i in range(self.__number_rows):
            gaussian[i] = np.exp(-((self.__wave_length[i] - center_gaussian) / float(sigma)) ** 2 / float(2))

        # we calculate the area of the gaussian and use it to obtain a normalized gaussian (dividing it with the area):
        gaussian_area = sum(gaussian)
        gaussian = [x / gaussian_area for x in gaussian]  # normalized gaussian

        # we convolve the initial flux with the normalized gaussian
        self.__flux = sp.signal.fftconvolve(initial_data2, gaussian, mode="same")
        # self.__flux = np.convolve(initial_data2, gaussian, mode="same")

        # plot (to check the data):
        '''plt.plot(self.__wave_length, gaussian)
        plt.show()'''

        fig, ax = plt.subplots()

        l1, = ax.plot(self.__wave_length, initial_data2)
        l2, = ax.plot(self.__wave_length, self.__flux)
        # l3, = ax.plot(self.__wave_length, gaussian)

        ax.legend((l1, l2), ('initial flux', 'final flux'), loc='upper right', shadow=False)
        ax.set_xlabel('wl')
        ax.set_ylabel('flux')
        ax.set_title('convolution')
        plt.show()

        '''plt.plot(self.__wave_length, initial_data2, 'k', label='original data')
        plt.plot(self.__wave_length, self.__flux, '.', label='filtered')
        # plt.plot(y6, ':', label='filtered, sigma=6')
        plt.legend()
        # plt.grid()
        plt.show()'''

    def do_plot(self):
        # basic plot (to check the data):
        plt.plot(self.__wave_length, self.__flux)
        plt.show()

    def save_to_file(self):
        print('Saving to file')
        # we stack both 1D np.arrays (final wave length and flux) to create a 2D np.array with two columns:
        final_data = np.column_stack((self.__wave_length, self.__flux))

        # save the 2D array in a pandas data frame
        data_frame = pd.DataFrame(final_data, columns=['wave_length', 'flux'])

        # save the data frame into a .csv file:
        data_frame.to_csv('file'+str(self.__T_eff)+'_'+str(self.__log_g)+'_modified.csv', index=False)

