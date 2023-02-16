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

    def instrumental_convolution(self, sigma, plot=False):
        print('Applying Instrumental Convolution')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.__initial_df['flux']

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.__initial_df['wl'].iloc[0]  # minimum wave length
        max_wl = self.__initial_df['wl'].iloc[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / float(2)  # mu = center of the gaussian

        # (implicit loop to) calculate the gaussian:
        gaussian = np.exp(-((self.__initial_df['wl'] - mu) / float(sigma)) ** 2 / float(2))

        # we calculate the area of the gaussian and use it to obtain a normalized gaussian (dividing it with the area):
        gaussian_area = sum(gaussian)
        gaussian = [x / gaussian_area for x in gaussian]  # normalized gaussian

        # we convolve the initial flux with the normalized gaussian
        self.__initial_df['flux'] = sp.signal.fftconvolve(initial_data, gaussian, mode="same")

        # if plot == True:
        if plot:
            print('Generating convolution plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(self.__initial_df['wl'], initial_data)
            l2, = ax.plot(self.__initial_df['wl'], self.__initial_df['flux'])

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

        # create a collection that will contain the positions of the PHOENIX wl in the standard wl array (with CARMENES
        # parameters), i.e., position of PHOENIX wl in between two standard wl
        df_positions = collections.deque()

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
        R = 94600  # resolution power
        resol = 2.3  # ??

        # sampling of the PHOENIX library
        delta_wl_phoenix = 0.01  # in A, [A]=Angstrom

        # create a variable that will contain the sum of the flux (used to verify flux conservation)
        sum_flux = 0.0
        # create a collection that will contain the flux in the new standard wl (after rebinning)
        flux = collections.deque()

        for i in range(len(self.__standard_df)):
            # point of interest: i
            wl_i = self.__standard_df['wl'].iloc[i]
            delta_wli = wl_i / (resol * R)
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
                elif (d <= delta_wli / 2.0 + delta_wl_phoenix / 2.0) & (d >= delta_wli / 2.0 - delta_wl_phoenix / 2.0):
                    alpha = (delta_wli / 2.0 + delta_wl_phoenix / 2.0 - d) / delta_wl_phoenix

                # sum of the flux that each point provides based on the previous conditions
                sum_flux += alpha * delta_wl_phoenix * compatible_wl['flux'].iloc[j]
                print(wl_i, compatible_wl['wl'].iloc[j], d, delta_wli, alpha)

            # flux corresponding to each standard wl_i
            flux_i = sum_flux / delta_wli
            # add each flux to the created collection
            flux.append(flux_i)

        # convert the collection into a list
        lst_final_flux = list(flux)
        # add the flux into de data frame with the standard wl as a new column
        self.__standard_df['flux'] = lst_final_flux

        # check is the flux is conserved
        initial_flux = sum(self.__initial_df['flux'])
        final_flux = sum(self.__standard_df['flux'])

        print(initial_flux, final_flux)

    def save_to_file(self):
        print('Saving to file in the NewLibrary folder')
        # save the modified file to a csv in the folder 'NewLibrary'
        self.__standard_df.to_csv('./NewLibrary/file_' + str(self.__temperature), index=False)


