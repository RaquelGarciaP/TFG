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
        # copy the standard wl into de final data frame as the wl ('x' axis)
        self.df['wl'] = self.__standard_wl['wl'].copy()

        self.__temperature_interpolator()
        self.__doppler_shift()
        self.__doppler_broadening(integral_check=True, plot_check=True)

    def __temperature_interpolator(self, integral_check=False, plot_check=False):
        print('Interpolation of Temperatures')

        val = float(self.__temperature) / 100.0
        floor = math.floor(val)
        ceil = math.ceil(val)

        # temperatures corresponding to library files
        if self.__temperature <= 7000.0:
            t1 = int(floor * 100)
            t2 = int(ceil * 100)

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

    def __doppler_shift(self, integral_check=False, plot_check=False):
        print('Applying Doppler Shift')
        c = 299792458.0  # light velocity (m/s)

        # we save the data before the Doppler shift (we only do this to do the check_plot)
        initial_data = self.df.copy()

        # Doppler shift
        self.df['wl'] = (1.0 + float(self.__radial_vel) / c) * initial_data['wl']

        # now we want to re-express the flux in the standardized wl
        print('Re-Standardizing the wavelength after Doppler shift')
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
        print('Applying Doppler Broadening')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.df['flux'].copy()

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.df['wl'].iloc[0]  # minimum wave length
        max_wl = self.df['wl'].iloc[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / 2.0  # mu = center of the gaussian

        # v sini = FWHM = 2*sqrt(2*ln2)*sigma = 2.35482 * sigma (in wl units: v sini * wl / c = FWHM)
        c = 299792458.0  # light velocity (m/s)
        ct = self.__vel_rotation / (2.35482 * c)
        sigma = ct * self.df['wl']

        gauss = collections.deque()

        # loop to calculate the gaussian:
        for i in range(len(self.df)):
            gauss.append((1.0 / (math.sqrt(2.0 * math.pi) * sigma.iloc[i])) * np.exp(-((self.df['wl'].iloc[i] - mu) / sigma.iloc[i]) ** 2 / 2.0))

        gaussian = list(gauss)

        # multiply each element of the normalized gaussian array by delta_wl_i (we do that because when we
        # calculate the convolution (an integral) we need use the trapezium method: multiplying each 'y' by its delta_x
        # and doing the sum of all of them gives the approximated integral)
        for i in range(len(gaussian)):
            gaussian[i] = gaussian[i] * self.__standard_wl['delta wl'].iloc[i]
        # gaussian = gaussian * self.__standard_wl['delta wl']
        # gaussian = [x * 0.01 for x in gaussian]

        # we convolve the initial flux with the normalized gaussian
        self.df['flux'] = sp.signal.fftconvolve(initial_data, gaussian, mode="same")

        # check of the flux conservation (integral conservation)
        if integral_check:
            print('Calculating flux conservation')
            integral_i = 0.0
            integral_f = 0.0

            for i in range(len(self.df)):
                integral_i += self.__standard_wl['delta wl'].iloc[i] * initial_data.iloc[i]

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

