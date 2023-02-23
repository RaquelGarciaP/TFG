import pandas as pd
import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import SingleFileModifier as sfm


class SpectraCombiner:

    def __init__(self, T1, T2, R21, L21, v_r1, v_r2, v_rot1, v_rot2):
        # save the introduced variables in class variables
        self.__T1 = T1  # temperature
        self.__T2 = T2
        self.__R21 = R21  # R2/R1 (radius of the stars)
        self.__L21 = L21  # L2/L1 (luminosities of the stars)
        # self.__inc = inc  # inclination of the orbital plane
        self.__v_r1 = v_r1  # radial velocity
        self.__v_r2 = v_r2
        self.__v_rot1 = v_rot1  # rotation velocity = v * sin(i), i: inclination
        self.__v_rot2 = v_rot2

        # initialize class SingleFileModifier for each star
        self.__sfm1 = sfm.SingleFileModifier(self.__T1, self.__v_r1, self.__v_rot1)
        # self.__sfm2 = sfm.SingleFileModifier(self.__T2, self.__v_r2, self.__v_rot2)

        # save the data frame corresponding to each star (we call the data frame obtained after calling SingleFileMod..)
        self.__df1 = self.__sfm1.df
        # self.__df2 = self.__sfm2.df

        # create the data frame for the combined spectra
        self.__combined_df = pd.DataFrame()

    def sum_spectra(self):
        print('Combining both fluxes')
        # save the wl in the final data frame copying the wl of the data frame corresponding to T1
        # (both data frames have standardized wl, we can choose any)
        self.__combined_df['wl'] = self.__df1['wl']

        # sum both fluxes taking into account the weight of each with R21 = R2/R1
        self.__combined_df['flux'] = self.__df1['flux'] + self.__R21**2 * self.__df2['flux']

    def plot(self):
        print('Generating combined spectra plot')

        plt.plot(self.__combined_df['wl'], self.__combined_df['flux'])
        plt.xlabel('Wavelength (A)')
        plt.ylabel('Flux')
        plt.title('Combined Spectra')
        plt.show()

    def save_to_file(self):
        print('Saving to file in the CombinedSpectra folder')
        # save the modified file to a csv in the folder 'NewLibrary'
        self.__combined_df.to_csv('./CombinedSpectra/combined_' + str(self.__T1) + '_' + str(self.__T2), index=False)

