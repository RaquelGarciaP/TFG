import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math


class Convolution:

    def __init__(self, sigma, data):
        self.__sigma = sigma
        self.__data = data

    def convolution(self):
        print('Applying Convolution')
        # we create a copy of the flux array (called initial_data2 bc it's the data b4 this modification):
        initial_data2 = self.__flux
        # we create the array that will contain the gaussian:
        gaussian = np.empty(self.__number_rows)

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.__wave_length[0]  # minimum wave length
        max_wl = self.__wave_length[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / float(2)

        # loop to calculate the gaussian:
        gaussian = np.exp(-((self.__wave_length - mu) / float(self.__sigma)) ** 2 / float(2))

        # we calculate the area of the gaussian and use it to obtain a normalized gaussian (dividing it with the area):
        gaussian_area = sum(gaussian)
        gaussian = [x / gaussian_area for x in gaussian]  # normalized gaussian

        # we convolve the initial flux with the normalized gaussian
        self.__flux = sp.signal.fftconvolve(initial_data2, gaussian, mode="same")
        # self.__flux = np.convolve(initial_data2, gaussian, mode="same")

    def plot(self):
        # plot (to check the data):
        fig, ax = plt.subplots()

        l1, = ax.plot(self.__wave_length, initial_data2)
        l2, = ax.plot(self.__wave_length, self.__flux)
        # l3, = ax.plot(self.__wave_length, gaussian)

        ax.legend((l1, l2), ('initial flux', 'final flux'), loc='upper right', shadow=False)
        ax.set_xlabel('wl')
        ax.set_ylabel('flux')
        ax.set_title('convolution')
        plt.show()

