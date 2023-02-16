import numpy as np
import pandas as pd
import scipy as sp
import math


class SingleFileModifier:

    def __init__(self, temperature, radial_vel, vel_rotation):

        self.__temperature = temperature
        self.__radial_vel = radial_vel
        self.__vel_rotation = vel_rotation

        # read the standard wavelength file (with CARMENES sampling)
        self.__standard_wl = pd.read_csv('./NewLibrary/standard_wl')

        # create the data frame that will contain the data after the modifications
        self.df = None

        self.__temperature_interpolator()
        self.__doppler_shift()
        self.__standardize_wl()
        self.__doppler_broadening()

    def __temperature_interpolator(self):
        print('Interpolation of Temperatures')

        val = float(self.__temperature) / 100.0
        floor = math.floor(val)
        ceil = math.ceil(val)

        # temperatures corresponding to library files
        t1 = int(floor * 100)
        t2 = int(ceil * 100)

        file_name_t1 = 'file_' + str(t1) + '.csv'
        file_name_t2 = 'file_' + str(t2) + '.csv'

        # we read the corresponding files
        df_t1 = pd.read_csv(file_name_t1)
        df_t2 = pd.read_csv(file_name_t2)

        # we do the interpolation (implicit loop)
        interpolator = (self.__temperature - float(t1)) / (float(t2) - float(t1))
        # resulting flux (after interpolation)
        flux_t3 = df_t1['flux'] + (df_t2['flux'] - df_t1['flux']) * interpolator

        # save the wl (standard and equal for both temperatures) and the resulting flux in a data frame (creating a
        # column for each: 'wl' and 'flux')
        self.df['wl'] = df_t1['wl']
        self.df['flux'] = flux_t3

    def __doppler_shift(self):
        print('Applying Doppler Shift')
        c = 299792458  # light velocity (m/s)

        self.df['wl'] = (1.0 + float(self.__radial_vel) / float(c)) * self.df['wl']

    def __standardize_wl(self):
        print('Re-Standardizing the wavelength after Doppler shift')

        # use numpy.interp() to obtain the interpolation of the flux with the standard wl
        self.df['flux'] = np.interp(self.__standard_wl['wl'], self.df['wl'], self.df['flux'])

    def __doppler_broadening(self):
        print('Applying Doppler Broadening')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.df['flux']

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.df['wl'].iloc[0]  # minimum wave length
        max_wl = self.df['wl'].iloc[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / float(2)  # mu = center of the gaussian

        # FWHM = delta_wl = vel_rotation * wl / c; FWHM = 2*sqrt(2*ln2)*sigma
        c = 299792458  # light velocity (m/s)
        wl = (5199.0 + 9601.0) / 2.0  # wl median
        FWHM = (self.__vel_rotation * wl) / c
        sigma = FWHM / 2.35482

        # (implicit loop to) calculate the gaussian:
        gaussian = np.exp(-((self.df['wl'] - mu) / float(sigma)) ** 2 / float(2))

        # we calculate the area of the gaussian and use it to obtain a normalized gaussian (dividing it with the area):
        gaussian_area = sum(gaussian)
        gaussian = [x / gaussian_area for x in gaussian]  # normalized gaussian

        # we convolve the initial flux with the normalized gaussian
        self.df['flux'] = sp.signal.fftconvolve(initial_data, gaussian, mode="same")

