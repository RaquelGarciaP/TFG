import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from bisect import bisect_left
import collections


class NewLibraryCreator:

    def __init__(self, file_name, temperature):
        self.__file_name = file_name
        self.__temperature = temperature
        # read the file with pandas from the folder 'OldLibrary' and save in the data frame to be modified
        self.__initial_df = pd.read_csv('./OldLibrary/' + self.__file_name, names=['wl', 'flux'])
        # read the standard wavelength file (with CARMENES sampling) and save it to a pandas data frame that will
        # contain the data modified to match CARMENES parameters
        self.__standard_df = pd.read_csv('./NewLibrary/standard_wl')

    def range_filter(self, rang_value1, rang_value2):
        print('Applying Range Filter')
        # create a boolean mask to choose the rows with the desired value
        mask = (self.__initial_df['wl'] >= rang_value1) & (self.__initial_df['wl'] <= rang_value2)

        # choose the rows with the mask
        # self.__filtered_df = self.__data_frame.loc[mask, :]
        self.__initial_df = self.__initial_df[mask]

    def instrumental_convolution(self, check_plot=False):
        print('Applying Instrumental Convolution')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.__initial_df['flux'].copy()

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.__initial_df['wl'].iloc[0]  # minimum wave length
        max_wl = self.__initial_df['wl'].iloc[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / float(2)  # mu = center of the gaussian

        R = 94600.0
        ct = 1.0 / (2.35482 * R)  # delta_lambda = lambda/R = FWHM = 2*sqrt(2*ln2)*sigma = 2.35482 * sigma
        sigma = ct * self.__initial_df['wl']

        gauss = collections.deque()

        # loop to calculate the gaussian:
        for i in range(len(self.__initial_df)):
            gauss.append(np.exp(-((self.__initial_df['wl'].iloc[i] - mu) / float(sigma.iloc[i])) ** 2 / float(2)))

        gaussian = list(gauss)

        # we calculate the area of the gaussian and use it to obtain a normalized gaussian (dividing by the area):
        gaussian_area = sum(gaussian)
        gaussian = [x / gaussian_area for x in gaussian]  # normalized gaussian

        # we convolve the initial flux with the normalized gaussian
        self.__initial_df['flux'] = sp.signal.fftconvolve(initial_data, gaussian, mode="same")

        # if plot == True:
        if check_plot:
            print('Generating convolution plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(self.__initial_df['wl'], initial_data)
            l2, = ax.plot(self.__initial_df['wl'], self.__initial_df['flux'])

            ax.legend((l1, l2), ('Initial flux', 'Final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Convolution check')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

    def rebinning(self, plot_check=False, integral_check=False):
        print('Applying Rebinning')

        # create a collection that will contain the positions of the PHOENIX wl in the standard wl array (with CARMENES
        # parameters), i.e., position of PHOENIX wl in between two standard wl
        df_positions = collections.deque()

        print('Searching the positions of the elements of the old array in the new wl array')
        # loop to obtain the positions of the wl
        for i in range(len(self.__initial_df)):
            # search the position of each element of the PHOENIX wl
            position = bisect_left(self.__standard_df['wl'], self.__initial_df['wl'].iloc[i])
            # fill the created collection
            df_positions.append(position)

        # convert de collection into a list
        lst = list(df_positions)
        # create a new column in the initial data frame that contains the position of each wl
        self.__initial_df['pos'] = lst

        # CARMENES sampling parameters
        R = 94600.0  # resolution power
        resol = 2.8  # pixels per resolution element

        # sampling of the PHOENIX library
        delta_wl_phoenix = 0.01  # in A, [A]=Angstrom

        # create a collection that will contain the flux in the new standard wl (after rebinning)
        flux = collections.deque()

        # create a collection that will contain the delta_wl of each standard wl
        delta_wl_standard = collections.deque()

        print('Calculating the flux in the new wl array')
        for i in range(len(self.__standard_df)):
            # create a variable that will contain the sum of the flux_i (used to verify flux conservation)
            sum_flux = 0.0

            # point of interest: i
            wl_i = self.__standard_df['wl'].iloc[i]
            delta_wli = wl_i / (resol * R)

            # add each delta to the created collection (this is necessary for the flux conservation check!)
            delta_wl_standard.append(delta_wli)

            # wl near to the point of interest
            compatible_wl = self.__initial_df.loc[(self.__initial_df['pos'] == i) | (self.__initial_df['pos'] == i + 1)]

            for j in range(len(compatible_wl)):
                # distance between the point of interest and the selected near point
                d = abs(wl_i - compatible_wl['wl'].iloc[j])

                # if the distance between both points is greater than both their delta_wl -> alpha = 0
                if d >= delta_wli / 2.0 + delta_wl_phoenix / 2.0:
                    alpha = 0.0

                # if the distance between both points is smaller than the rest of their delta_wl -> alpha = 1
                elif d <= delta_wli / 2.0 - delta_wl_phoenix / 2.0:
                    alpha = 1.0

                # if the distance value is in between both intervals
                # (d <= delta_wli / 2.0 + delta_wl_phoenix / 2.0) & (d >= delta_wli / 2.0 - delta_wl_phoenix / 2.0)
                else:
                    alpha = (delta_wli / 2.0 + delta_wl_phoenix / 2.0 - d) / delta_wl_phoenix

                # sum of the flux that each point provides based on the previous conditions
                sum_flux += alpha * delta_wl_phoenix * compatible_wl['flux'].iloc[j]

            # flux corresponding to each standard wl_i
            flux_i = sum_flux / delta_wli
            # add each flux to the created collection
            flux.append(flux_i)

        # convert the collection into a list
        lst_final_flux = list(flux)
        # add the flux into de data frame with the standard wl as a new column
        self.__standard_df['flux'] = lst_final_flux

        # first check of the flux conservation
        # if plot_check == True:
        if plot_check:
            print('Generating flux plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(self.__initial_df['wl'], self.__initial_df['flux'])
            l2, = ax.plot(self.__standard_df['wl'], self.__standard_df['flux'])

            ax.legend((l1, l2), ('Initial flux', 'Final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Rebinning plot check')
            plt.show()

        # if plot_check == False: (correct way to express it -> if not plot_check:)
        else:
            pass

        if integral_check:
            integral_i = 0.0
            integral_f = 0.0

            for i in range(len(self.__initial_df)):
                integral_i += delta_wl_phoenix * self.__initial_df['flux'].iloc[i]

            for i in range(len(self.__standard_df)):
                integral_f += delta_wl_standard[i] * self.__standard_df['flux'].iloc[i]

            diff = abs(integral_i - integral_f)
            print('Integral initial state: ', integral_i)
            print('Integral final state: ', integral_f)
            print('Difference: ', diff, '   Difference / initial flux: ', diff / integral_i)

        else:
            pass

    def save_to_file(self):
        print('Saving to file in the NewLibrary folder')
        # save the modified file to a csv in the folder 'NewLibrary'
        self.__standard_df.to_csv('./NewLibrary/file_' + str(self.__temperature), index=False)


