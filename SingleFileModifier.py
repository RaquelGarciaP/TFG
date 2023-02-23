import numpy as np
import pandas as pd
import scipy as sp
import math
import collections
import matplotlib.pyplot as plt


class SingleFileModifier:

    def __init__(self, temperature, radial_vel, vel_rotation):

        self.__temperature = temperature
        self.__radial_vel = radial_vel
        self.__vel_rotation = vel_rotation  # rotation velocity = v * sin(i), i: inclination

        # read the standard wavelength file (with CARMENES sampling)
        self.__standard_wl = pd.read_csv('./NewLibrary/standard_wl')

        # create the data frame that will contain the data after the modifications
        self.df = pd.DataFrame()

        self.__temperature_interpolator()
        self.__doppler_shift()
        self.__doppler_broadening(check_plot=True)

    def __temperature_interpolator(self, check_plot=False):
        print('Interpolation of Temperatures')

        val = float(self.__temperature) / 100.0
        floor = math.floor(val)
        ceil = math.ceil(val)

        # temperatures corresponding to library files
        t1 = int(floor * 100)
        t2 = int(ceil * 100)

        file_name_t1 = 'file_' + str(t1)
        file_name_t2 = 'file_' + str(t2)

        # we read the corresponding files
        df_t1 = pd.read_csv('./NewLibrary/' + file_name_t1)
        df_t2 = pd.read_csv('./NewLibrary/' + file_name_t2)

        print(file_name_t1, file_name_t2)

        # we do the interpolation (implicit loop)
        interpolator = (self.__temperature - float(t1)) / (float(t2) - float(t1))
        # resulting flux (after interpolation)
        self.df['flux'] = df_t1['flux'] + (df_t2['flux'] - df_t1['flux']) * interpolator

        # save the wl (standard and equal for both temperatures) and the resulting flux in a data frame (creating a
        # column for each: 'wl' and 'flux')
        self.df['wl'] = df_t1['wl']
        # self.df['flux'] = flux_t3

        if check_plot:
            print('Generating temperature interpolation check plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(df_t1['wl'], df_t1['flux'])
            l2, = ax.plot(df_t2['wl'], df_t2['flux'])
            l3, = ax.plot(self.df['wl'], self.df['flux'])

            ax.legend((l1, l2, l3), ('T1', 'T2', 'Combined T'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Temperature interpolation check')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

    def __doppler_shift(self, check_plot=False):
        print('Applying Doppler Shift')
        c = 299792458  # light velocity (m/s)

        # we save the data before the Doppler shift ( we only do this to do the check_plot)
        initial_data = self.df.copy()

        # Doppler shift
        self.df['wl'] = (1.0 + float(self.__radial_vel) / float(c)) * initial_data['wl']

        # now we want to re-express the flux in the standardized wl
        print('Re-Standardizing the wavelength after Doppler shift')
        # use numpy.interp() to obtain the interpolation of the flux with the standard wl -> the flux corresponding
        # to the standardized wl
        self.df['flux'] = np.interp(self.__standard_wl['wl'], self.df['wl'], self.df['flux'])
        # set the wavelength to be equal to the standardized one (we can do that bc now the flux corresponds to that wl)
        self.df['wl'] = self.__standard_wl['wl']

        # if plot == True:
        if check_plot:
            print('Generating Doppler shift check plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(initial_data['wl'], initial_data['flux'])
            l2, = ax.plot(self.df['wl'], self.df['flux'])

            ax.legend((l1, l2), ('Initial flux', 'Final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Doppler shift check')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

    def __doppler_broadening(self, check_plot=False):
        print('Applying Doppler Broadening')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.df['flux'].copy()

        # plt.plot(self.df['wl'], initial_data)

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.df['wl'].iloc[0]  # minimum wave length
        max_wl = self.df['wl'].iloc[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / float(2)  # mu = center of the gaussian

        # FWHM = 2*sqrt(ln2) * delta_wl = 2*sqrt(ln2) * vel_rotation * wl / c -> sigma = vel_rotation * wl / c * sqrt(2)
        c = 299792458  # light velocity (m/s)
        ct = self.__vel_rotation / (float(c) * math.sqrt(2))
        sigma = 0.05  # ct * self.df['wl']

        gauss = collections.deque()

        # loop to calculate the gaussian:
        for i in range(len(self.df)):
            gauss.append((1.0 / (math.sqrt(2.0 * math.pi) * sigma)) * np.exp(-((self.df['wl'].iloc[i] - mu) / float(sigma)) ** 2 / float(2)))

        gaussian = list(gauss)

        # we calculate the area of the gaussian and use it to obtain a normalized gaussian (dividing it with the area):
        gaussian_area = 0.0
        for i in range(len(self.__standard_wl)):
            gaussian_area += self.__standard_wl['delta wl'].iloc[i] * gaussian[i]
        print(gaussian_area)
        # gaussian = [x / gaussian_area for x in gaussian]  # normalized gaussian

        # we convolve the initial flux with the normalized gaussian
        self.df['flux'] = sp.signal.fftconvolve(initial_data, gaussian, mode="same")

        # plt.plot(self.df['wl'], self.df['flux'])

        # if plot == True:
        if check_plot:
            print('Generating Doppler broadening check plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(self.df['wl'], initial_data)
            l2, = ax.plot(self.df['wl'], self.df['flux'])

            ax.legend((l1, l2), ('Initial flux', 'Final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Doppler broadening check')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

