import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from bisect import bisect_left


class NewLibraryCreator:

    def __init__(self, file_name, temperature):
        self.__file_name = file_name
        self.__temperature = temperature
        # read the file with pandas from the folder 'OldLibrary' and save in the data frame to be modified
        self.__data_frame = pd.read_csv('./OldLibrary/' + self.__file_name, names=['wl', 'flux'])
        # create a class variable to save the rebinned data frame (with CARMENES sampling)
        self.__rebinned_df = None

    def range_filter(self, rang_value1, rang_value2):
        print('Applying Range Filter')
        # create a boolean mask to choose the rows with the desired value
        mask = (self.__data_frame['wl'] >= rang_value1) & (self.__data_frame['wl'] <= rang_value2)

        # choose the rows with the mask
        # self.__filtered_df = self.__data_frame.loc[mask, :]
        self.__data_frame = self.__data_frame[mask]

    def instrumental_convolution(self, sigma, plot=False):
        print('Applying Instrumental Convolution')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.__data_frame['flux']

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.__data_frame['wl'].iloc[0]  # minimum wave length
        max_wl = self.__data_frame['wl'].iloc[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / float(2)  # mu = center of the gaussian

        # (implicit loop to) calculate the gaussian:
        gaussian = np.exp(-((self.__data_frame['wl'] - mu) / float(sigma)) ** 2 / float(2))

        # we calculate the area of the gaussian and use it to obtain a normalized gaussian (dividing it with the area):
        gaussian_area = sum(gaussian)
        gaussian = [x / gaussian_area for x in gaussian]  # normalized gaussian

        # we convolve the initial flux with the normalized gaussian
        self.__data_frame['flux'] = sp.signal.fftconvolve(initial_data, gaussian, mode="same")

        # if plot == True:
        if plot:
            print('Generating convolution plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(self.__data_frame['wl'], initial_data)
            l2, = ax.plot(self.__data_frame['wl'], self.__data_frame['flux'])

            ax.legend((l1, l2), ('initial flux', 'final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('wl')
            ax.set_ylabel('flux')
            ax.set_title('convolution')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

    def rebinning(self):
        print('Applying Rebinning')

        # the first thing is creating the new standard wavelength array (with the new sampling)
        R = 94600  # CARMENES resolution power


    def save_to_file(self):
        print('Saving to file in the NewLibrary folder')
        # save the modified file to a csv in the folder 'NewLibrary'
        self.__data_frame.to_csv('./NewLibrary/file_' + self.__temperature, index=False)


