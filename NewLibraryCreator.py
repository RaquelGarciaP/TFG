import pandas as pd
import numpy as np
import scipy as sp
import math
import matplotlib.pyplot as plt
from bisect import bisect_left
import collections


class NewLibraryCreator:

    def __init__(self, file_name, temperature):
        self.__file_name = file_name
        self.__temperature = temperature
        # read the file with pandas from the folder 'OldLibrary' and save in the data frame to be modified
        self.__initial_df = pd.read_csv('./OldLibrary/' + self.__file_name, names=['wl', 'flux'])
        # read the standard wavelength file (with CARMENES sampling) and save it to a pandas data frame
        self.__standard_wl = pd.read_csv('./NewLibrary/standard_wl')
        # data frame that will contain the data after the re-binning (modified to match CARMENES parameters)
        self.__final_df = pd.DataFrame()
        # copy the standard wl into de final data frame as the wl ('x' axis)
        self.__final_df['wl'] = self.__standard_wl['wl'].copy()

        # CARMENES sampling parameters
        self.__R = 94600.0  # resolution power
        # self.__resol = 2.8  # pixels per resolution element

        # PHOENIX library sampling parameters
        self.__delta_wl_phoenix = 0.01  # in A, [A]=Angstrom

    def range_filter(self, rang_value1, rang_value2):
        print('Applying Range Filter')
        # create a boolean mask to choose the rows with the desired value
        mask = (self.__initial_df['wl'] >= rang_value1) & (self.__initial_df['wl'] <= rang_value2)

        # choose the rows with the mask
        self.__initial_df = self.__initial_df[mask]

    def instrumental_convolution(self, integral_check=False, plot_check=False):
        print('Applying Instrumental Convolution')
        # we create a copy of the flux array (called initial_data bc it's the data b4 this modification):
        initial_data = self.__initial_df['flux'].copy()

        # we center the gaussian in the middle of the wave length axis:
        min_wl = self.__initial_df['wl'].iloc[0]  # minimum wave length
        max_wl = self.__initial_df['wl'].iloc[-1]  # maximum wave length
        mu = min_wl + (max_wl - min_wl) / 2.0  # mu = center of the gaussian

        # sigma of the gaussian
        ct = 1.0 / (2.35482 * self.__R)  # delta_lambda = lambda/R = FWHM = 2*sqrt(2*ln2)*sigma = 2.35482 * sigma
        sigma = ct * self.__initial_df['wl']

        # calculus of the gaussian (implicit loop):
        # also, we multiply each element of the normalized gaussian by delta_wl_i (we do that because when we
        # calculate the convolution (an integral) we need use the trapezium method: multiplying each 'y' by its delta_x
        # and doing the sum of all of them gives the approximated integral)
        gaussian = self.__delta_wl_phoenix * (1.0 / (math.sqrt(2.0 * math.pi) * sigma)) * \
                   np.exp(-((self.__initial_df['wl'] - mu) / sigma) * ((self.__initial_df['wl'] - mu) / sigma) / 2.0)

        # we convolve the initial flux with the normalized gaussian
        self.__initial_df['flux'] = sp.signal.fftconvolve(initial_data, gaussian, mode="same")

        # check of the flux conservation (integral conservation)
        if integral_check:
            print('Calculating flux conservation')
            integral_i = 0.0
            integral_f = 0.0

            for i in range(len(self.__initial_df)):
                integral_i += self.__delta_wl_phoenix * initial_data.iloc[i]
                integral_f += self.__delta_wl_phoenix * self.__initial_df['flux'].iloc[i]

            diff = abs(integral_i - integral_f)
            print(' Flux integral initial state: ', integral_i)
            print(' Flux integral final state: ', integral_f)
            print(' Difference: ', diff, '   Difference / initial flux: ', diff / integral_i)

        else:
            pass

        # if plot == True:
        if plot_check:
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

    def rebinning(self, integral_check=False, plot_check=False):
        print('Applying Rebinning')

        # create a collection that will contain the positions of the PHOENIX wl in the standard wl array (with CARMENES
        # parameters), i.e., position of PHOENIX wl in between two standard wl
        df_positions = collections.deque()

        print('Searching the positions of the elements of the old array in the new wl array')
        # loop to obtain the positions of the wl
        for i in range(len(self.__initial_df)):
            # search the position of each element of the PHOENIX wl
            position = bisect_left(self.__standard_wl['wl'], self.__initial_df['wl'].iloc[i])
            # fill the created collection
            df_positions.append(position)

        # convert de collection into a list
        lst = list(df_positions)
        # create a new column in the initial data frame that contains the position of each wl
        self.__initial_df['pos'] = lst

        # todo: aquest càlcul funciona creant un np.array.empty amb la dimensió de standard_wl i sobreescribint cada
        #  flux[i] pel valor corresponent -> comprovar quin càlcul és més ràpid (probablement amb np)
        # create a collection that will contain the flux in the new standard wl (after rebinning)
        flux = collections.deque()

        print('Calculating the flux in the new wl array')
        for i in range(len(self.__standard_wl)):
            # create a variable that will contain the sum of the flux_i (used to verify flux conservation)
            sum_flux = 0.0

            # point of interest: i
            wl_i = self.__standard_wl['wl'].iloc[i]
            delta_wli = self.__standard_wl['delta wl'].loc[i]

            # wl near to the point of interest
            compatible_wl = self.__initial_df.loc[(self.__initial_df['pos'] == i) | (self.__initial_df['pos'] == i + 1)]

            for j in range(len(compatible_wl)):
                # distance between the point of interest and the selected near point
                d = abs(wl_i - compatible_wl['wl'].iloc[j])

                # if the distance between both points is greater than both their delta_wl -> alpha = 0
                if d >= delta_wli / 2.0 + self.__delta_wl_phoenix / 2.0:
                    alpha = 0.0

                # if the distance between both points is smaller than the rest of their delta_wl -> alpha = 1
                elif d <= delta_wli / 2.0 - self.__delta_wl_phoenix / 2.0:
                    alpha = 1.0

                # if the distance value is in between both intervals
                # (d <= delta_wli / 2.0 + delta_wl_phoenix / 2.0) & (d >= delta_wli / 2.0 - delta_wl_phoenix / 2.0)
                else:
                    alpha = (delta_wli / 2.0 + self.__delta_wl_phoenix / 2.0 - d) / self.__delta_wl_phoenix

                # sum of the flux that each point provides based on the previous conditions
                sum_flux += alpha * self.__delta_wl_phoenix * compatible_wl['flux'].iloc[j]

            # flux corresponding to each standard wl_i
            flux_i = sum_flux / delta_wli
            # add each flux to the created collection
            flux.append(flux_i)

        # convert the collection into a list
        lst_final_flux = list(flux)
        # add the flux into de final data frame (with CARMENES sampling) as a new column
        self.__final_df['flux'] = lst_final_flux

        # check of the flux conservation (integral conservation)
        if integral_check:
            print('Calculating flux conservation')
            integral_i = 0.0
            integral_f = 0.0

            for i in range(len(self.__initial_df)):
                integral_i += self.__delta_wl_phoenix * self.__initial_df['flux'].iloc[i]

            for i in range(len(self.__standard_wl)):
                integral_f += self.__standard_wl['delta wl'].iloc[i] * self.__final_df['flux'].iloc[i]

            diff = abs(integral_i - integral_f)
            print(' Flux integral initial state: ', integral_i)
            print(' Flux integral final state: ', integral_f)
            print(' Difference: ', diff, '   Difference / initial flux: ', diff / integral_i)

        else:
            pass

        # if plot_check == True:
        if plot_check:
            print('Generating flux plot')
            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(self.__initial_df['wl'], self.__initial_df['flux'])
            l2, = ax.plot(self.__final_df['wl'], self.__final_df['flux'])

            ax.legend((l1, l2), ('Initial flux', 'Final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Rebinning plot check')
            plt.show()

        # if plot_check == False: (correct way to express it -> if not plot_check:)
        else:
            pass

    def save_to_file(self):
        print('Saving to file in the NewLibrary folder')
        # save the modified file to a csv in the folder 'NewLibrary'
        self.__final_df.to_csv('./NewLibrary/file_' + str(self.__temperature), index=False)


