import numpy as np
import pandas as pd
import scipy as sp
import math
import matplotlib.pyplot as plt


class SingleFileModifier:

    def __init__(self, standard_wl, temperature, vel_rotation):

        self.__temperature = temperature
        # self.__radial_vel = radial_vel
        self.__vel_rotation = vel_rotation  # rotation velocity = v * sin(i), i: inclination

        # save the standard wavelength df (it is an input, so we only read the file one time -in main-)
        self.__standard_wl = standard_wl

        # create the data frame that will contain the data after the modifications
        self.df = pd.DataFrame()

        # copy the standard wl into de final data frame as the wl ('x' axis)
        self.df['wl'] = self.__standard_wl['wl'].copy()

        # apply all the functions of the class
        self.__temperature_interpolator()
        # self.__doppler_shift()
        self.__doppler_broadening()

    def __temperature_interpolator(self, integral_check=False, plot_check=False):
        # print('Interpolation of Temperatures')

        val = float(self.__temperature) / 100.0
        floor = math.floor(val)
        ceil = math.ceil(val)

        # temperatures corresponding to library files
        if self.__temperature <= 7000.0:
            t1 = int(floor * 100)
            t2 = int(ceil * 100)

        # for T >= 7000 the difference between temperatures of the library changes
        else:
            if (floor % 2) == 0:
                floor = floor
            else:
                floor = floor - 1

            if (ceil % 2) == 0:
                ceil = ceil
            else:
                ceil = ceil + 1

            t1 = int(floor * 100)
            t2 = int(ceil * 100)

        file_name_t1 = 'file_' + str(t1)
        file_name_t2 = 'file_' + str(t2)

        # we read the corresponding files
        df_t1 = pd.read_csv('./NewLibrary/' + file_name_t1)
        df_t2 = pd.read_csv('./NewLibrary/' + file_name_t2)

        ############################################# NEW #####################################################
        '''# copy the wave length of one of the files to standard_wl (both files have the standardized wl)
        self.__standard_wl = df_t1['wl'].copy()
        # copy the standard wl into de final data frame as the wl ('x' axis)
        self.df['wl'] = self.__standard_wl['wl'].copy()'''
        ############################################# NEW #####################################################

        print('Interpolating with files: ', file_name_t1, ' and ', file_name_t2)

        # we do the interpolation (implicit loop)
        interpolator = (self.__temperature - float(t1)) / (float(t2) - float(t1))
        # we save resulting flux (after interpolation) in the final data frame
        self.df['flux'] = df_t1['flux'] + (df_t2['flux'] - df_t1['flux']) * interpolator

        if integral_check:
            print('Calculating flux conservation')
            integral_1 = 0.0
            integral_2 = 0.0
            integral_f = 0.0

            for i in range(len(df_t1)):
                integral_1 += self.__standard_wl['wl'].iloc[i] * df_t1['flux'].iloc[i]

            for i in range(len(df_t2)):
                integral_2 += self.__standard_wl['wl'].iloc[i] * df_t2['flux'].iloc[i]

            for i in range(len(self.df)):
                integral_f += self.__standard_wl['wl'].iloc[i] * self.df['flux'].iloc[i]

            interpol_integral_flux = integral_1 + (integral_2 - integral_1) * interpolator
            diff = abs(interpol_integral_flux - integral_f)
            print(' Sum of fluxes for T1 and T2 (before interpolation): ', interpol_integral_flux)
            print(' Flux integral of the desired T (after interpolation): ', integral_f)
            print(' Difference: ', diff, '   Difference / initial flux: ', diff / interpol_integral_flux)

        else:
            pass

        if plot_check:
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

    def doppler_shift(self, radial_vel, integral_check=False, plot_check=False):
        # print('Applying Doppler Shift')
        c = 299792458.0  # light velocity (m/s)

        # we save the data before the Doppler shift (we only do this to do the check_plot)
        initial_data = self.df.copy()

        # Doppler shift
        self.df['wl'] = (1.0 + float(radial_vel) / c) * initial_data['wl']

        # now we want to re-express the flux in the standardized wl
        # print('Re-Standardizing the wavelength after Doppler shift')
        # use numpy.interp() to obtain the interpolation of the flux with the standard wl -> the flux corresponding
        # to the standardized wl
        self.df['flux'] = np.interp(self.__standard_wl['wl'], self.df['wl'], self.df['flux'])
        # set the wavelength to be equal to the standardized one (we can do that bc now the flux corresponds to that wl)
        self.df['wl'] = self.__standard_wl['wl'].copy()

        # check of the flux conservation (integral conservation)
        if integral_check:
            print('Calculating flux conservation')
            integral_i = 0.0
            integral_f = 0.0

            for i in range(len(self.df)):
                integral_i += self.__standard_wl['delta wl'].iloc[i] * initial_data['flux'].iloc[i]

            for i in range(len(self.df)):
                integral_f += self.__standard_wl['delta wl'].iloc[i] * self.df['flux'].iloc[i]

            diff = abs(integral_i - integral_f)
            print(' Flux integral initial state: ', integral_i)
            print(' Flux integral final state: ', integral_f)
            print(' Difference: ', diff, '   Difference / initial flux: ', diff / integral_i)

        else:
            pass

        # if plot == True:
        if plot_check:
            print('Generating Doppler shift check plot')

            # USE ONLY IF WE WANT TO PLOT A SMALL INTERVAL OF THE TOTAL DATA FRAME
            '''mask = (initial_data['wl'] >= 6340.0) & (initial_data['wl'] <= 6380.0)
            initial_data = initial_data[mask]
            mask = (self.df['wl'] >= 6340.0) & (self.df['wl'] <= 6380.0)
            df_copy = self.df[mask]'''

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

    def __doppler_broadening(self, integral_check=False, plot_check=False):
        # print('Applying Doppler Broadening')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.df.copy()

        # we center the gaussian in the middle of the wave length axis:
        middle = self.df['wl'].iloc[81200]  # wave length in the center of the wl array (81200 middle position)
        mu = middle

        # v sini = FWHM = 2*sqrt(2*ln2)*sigma = 2.35482 * sigma (in wl units: v sini * wl / c = FWHM)
        c = 299792458.0  # light velocity (m/s)
        ct = self.__vel_rotation / (2.35482 * c)
        sigma = ct * self.df['wl']

        # calculus of the gaussian (implicit loop):
        # also, we multiply each element of the normalized gaussian by delta_wl_i (we do that because when we
        # calculate the convolution (an integral) we need use the trapezium method: multiplying each 'y' by its delta_x
        # and doing the sum of all of them gives the approximated integral)
        gaussian = self.__standard_wl['delta wl'] * (1.0 / (math.sqrt(2.0 * math.pi) * sigma)) \
                   * np.exp(-((self.df['wl'] - mu) / sigma) * ((self.df['wl'] - mu) / sigma) / 2.0)

        # we convolve the initial flux with the normalized gaussian
        self.df['flux'] = sp.signal.fftconvolve(initial_data['flux'], gaussian, mode="same")

        # check of the flux conservation (integral conservation)
        if integral_check:
            print('Calculating flux conservation')
            integral_i = 0.0
            integral_f = 0.0

            for i in range(len(self.df)):
                integral_i += self.__standard_wl['delta wl'].iloc[i] * initial_data['flux'].iloc[i]

            for i in range(len(self.df)):
                integral_f += self.__standard_wl['delta wl'].iloc[i] * self.df['flux'].iloc[i]

            diff = abs(integral_i - integral_f)
            print(' Flux integral initial state: ', integral_i)
            print(' Flux integral final state: ', integral_f)
            print(' Difference: ', diff, '   Difference / initial flux: ', diff / integral_i)

        else:
            pass

        # if plot == True:
        if plot_check:
            print('Generating Doppler broadening check plot')

            # USE ONLY IF WE WANT TO PLOT A SMALL INTERVAL OF THE TOTAL DATA FRAME
            '''mask = (initial_data['wl'] >= 6340.0) & (initial_data['wl'] <= 6380.0)
            initial_data = initial_data[mask]
            mask = (self.df['wl'] >= 6340.0) & (self.df['wl'] <= 6380.0)
            df_copy = self.df[mask]'''

            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(initial_data['wl'], initial_data['flux'])
            l2, = ax.plot(self.df['wl'], self.df['flux'])

            ax.legend((l1, l2), ('Initial flux', 'Final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Doppler broadening check')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

