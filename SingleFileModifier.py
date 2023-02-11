import numpy as np
import pandas as pd
import scipy as sp
import math
import matplotlib.pyplot as plt


class SingleFileModifier:

    def __init__(self, temperature):

        self.__temperature = temperature

        # file that we want to read:
        self.__file_name = 'file_' + str(self.__temperature) + '.csv'

        # we read the file using the library pandas
        print('Reading the file')
        self.__initial_df = pd.read_csv(self.__file_name, names=['wl', 'flux'])

        # we obtain the number of rows of our data (number of data we have per column); useful for iterations
        self.__number_rows = len(self.__initial_df)

        # save the initial data in the class variables for the wl and flux (will be MODIFIED)
        print('Saving the data in the class variables')
        self.__wave_length = self.__initial_df['wl']
        self.__flux = self.__initial_df['flux']

    def doppler_shift(self, radial_vel):
        c = 299792458  # light velocity (m/s)

        print('Applying Doppler Shift')
        # loop to apply the Doppler shift:
        for i in range(self.__number_rows):
            self.__wave_length[i] = (1 + float(radial_vel) / float(c)) * self.__wave_length[i]

    def convolution(self, sigma, plot=False):
        print('Applying Convolution')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.__flux

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.__wave_length[0]  # minimum wave length
        max_wl = self.__wave_length[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / float(2)  # mu = center of the gaussian

        # (implicit loop to) calculate the gaussian:
        gaussian = np.exp(-((self.__wave_length - mu) / float(sigma)) ** 2 / float(2))

        # we calculate the area of the gaussian and use it to obtain a normalized gaussian (dividing it with the area):
        gaussian_area = sum(gaussian)
        gaussian = [x / gaussian_area for x in gaussian]  # normalized gaussian

        # we convolve the initial flux with the normalized gaussian
        self.__flux = sp.signal.fftconvolve(initial_data, gaussian, mode="same")

        # if plot == True:
        if plot:
            print('Generating convolution plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(self.__wave_length, initial_data)
            l2, = ax.plot(self.__wave_length, self.__flux)

            ax.legend((l1, l2), ('initial flux', 'final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('wl')
            ax.set_ylabel('flux')
            ax.set_title('convolution')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

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
        data_frame.to_csv('file' + str(self.__temperature) + '_modified.csv', index=False)

