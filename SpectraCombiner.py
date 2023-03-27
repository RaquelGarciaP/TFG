import pandas as pd
import matplotlib.pyplot as plt
from SingleFileModifier import SingleFileModifier


class SpectraCombiner:

    def __init__(self, T1, T2, R21, v_r1, v_r2, v_rot1, v_rot2):
        # save the introduced variables in class variables
        self.__T1 = T1  # temperature
        self.__T2 = T2
        self.__R21 = R21  # R2/R1 (radius of the stars)
        # self.__L21 = L21  # L2/L1 (luminosities of the stars)
        # self.__inc = inc  # inclination of the orbital plane
        self.__v_r1 = v_r1  # radial velocity
        self.__v_r2 = v_r2
        self.__v_rot1 = v_rot1  # rotation velocity = v * sin(i), i: inclination
        self.__v_rot2 = v_rot2

        # initialize class SingleFileModifier for each star
        self.__sfm1 = SingleFileModifier(self.__T1, self.__v_r1, self.__v_rot1)
        self.__sfm2 = SingleFileModifier(self.__T2, self.__v_r2, self.__v_rot2)

        # save the data frame corresponding to each star (we call the data frame obtained after init SingleFileMod..)
        self.__df1 = self.__sfm1.df.copy()
        self.__df2 = self.__sfm2.df.copy()

        # read the standard wavelength file
        self.__standard_wl = pd.read_csv('./NewLibrary/standard_wl')

        # create the data frame for the combined spectra
        self.combined_df = pd.DataFrame()

        # sum spectra (modifies self.combined_df)
        self.__sum_spectra()

    def __sum_spectra(self, integral_check=False, plot_check=False):
        print('Combining both fluxes')

        # the wl in the combined df will correspond to the standardized wl
        self.combined_df['wl'] = self.__standard_wl['wl'].copy()

        # sum both fluxes taking into account the weight of each with R21 = R2/R1
        self.combined_df['flux'] = self.__df1['flux'] + self.__R21 ** 2 * self.__df2['flux']

        if integral_check:
            print('Calculating flux conservation')
            integral_1 = 0.0
            integral_2 = 0.0
            integral_f = 0.0

            for i in range(len(self.__df1)):
                integral_1 += self.__standard_wl['wl'].iloc[i] * self.__df1['flux'].iloc[i]

            for i in range(len(self.__df2)):
                integral_2 += self.__standard_wl['wl'].iloc[i] * self.__df2['flux'].iloc[i]

            for i in range(len(self.combined_df)):
                integral_f += self.__standard_wl['wl'].iloc[i] * self.combined_df['flux'].iloc[i]

            interpol_integral_flux = integral_1 + self.__R21**2 * integral_2
            diff = abs(interpol_integral_flux - integral_f)
            print(' Sum of fluxes for T1 and T2 (before interpolation): ', interpol_integral_flux)
            print(' Flux integral of the desired T (after interpolation): ', integral_f)
            print(' Difference: ', diff, '   Difference / initial flux: ', diff / interpol_integral_flux)

        else:
            pass

        if plot_check:
            print('Generating temperature interpolation check plot')

            # USE ONLY IF WE WANT TO PLOT A SMALL INTERVAL OF THE TOTAL DATA FRAME
            '''mask = (self.__df1['wl'] >= 6340.0) & (self.__df1['wl'] <= 6380.0)
            df1_copy = self.__df1[mask]
            mask = (self.__df2['wl'] >= 6340.0) & (self.__df2['wl'] <= 6380.0)
            df2_copy = self.__df2[mask]
            mask = (self.__combined_df['wl'] >= 6340.0) & (self.__combined_df['wl'] <= 6380.0)
            dfcomb_copy = self.__combined_df[mask]'''

            # plot (to check the data):
            fig, ax = plt.subplots()

            l1, = ax.plot(self.__df1['wl'], self.__df1['flux'])
            l2, = ax.plot(self.__df2['wl'], self.__R21**2 * self.__df2['flux'])
            l3, = ax.plot(self.combined_df['wl'], self.combined_df['flux'])
            '''l1, = ax.plot(df1_copy['wl'], df1_copy['flux'])
            l2, = ax.plot(df2_copy['wl'], self.__R21 ** 2 * df2_copy['flux'])
            l3, = ax.plot(dfcomb_copy['wl'], dfcomb_copy['flux'])'''

            ax.legend((l1, l2, l3), ('T1', 'T2', 'Joined Spectra'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Spectra Sum check')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

    def plot(self):
        print('Generating combined spectra plot')

        plt.plot(self.combined_df['wl'], self.combined_df['flux'])
        plt.xlabel('Wavelength (A)')
        plt.ylabel('Flux')
        plt.title('Combined Spectra')
        plt.show()

    def save_to_file(self, path: str, file_name: str):
        print('Saving to file in the CombinedSpectra folder')
        # save the modified file to a csv in the folder 'NewLibrary'
        self.combined_df.to_csv(path + '/' + file_name + '.csv', index=False)

