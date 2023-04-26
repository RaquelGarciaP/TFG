import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from SingleFileModifier import SingleFileModifier
from KeplerianOrbit import KeplerianOrbit
from Rassine import rassine

start_time = time.time()


class SpectraCombiner:

    def __init__(self, standard_wl, general_params, orbital_params, num_t):

        # save the standard wavelength df (it is an input, so we only read the file one time -in main-)
        self.__standard_wl = standard_wl

        # general parameters of the stars
        self.__T1, self.__T2, self.__R21, self.__v_rot1, self.__v_rot2 = general_params
        # T: temperature of the star
        # R21 = R2/R1: ratio between the radius of each star
        # v_rot: rotational velocity

        # orbital parameters
        self.__period, self.__K1, self.__K2, self.__ecc, self.__omega1, self.__omega2, self.__t_peri = orbital_params
        # ####self.__period2, self.__K2, self.__ecc2, self.__omega2, self.__t_peri2 = orbital_params2
        # period: orbital period
        # K: radial velocity semi-amplitude
        # ecc: eccentricity of the orbit
        # omega: angle of periastron
        # t_peri: time of periastron_passage

        # number of steps in t array
        self.__num_t = num_t

        # create the data frame for the combined spectra (each column will contain the spectra for a concrete time)
        self.final_df = pd.DataFrame()
        self.final_df['wave'] = self.__standard_wl['wl'].copy()

        # time evolution (self.final_df will be filled with the combined spectra for each time)
        self.__time_evolution()

        # continuum normalization
        self.__continuum_normalization()

        # final time
        end_time = time.time()
        print('FINAL TIME: ', end_time-start_time)

    def __time_evolution(self):

        # time array creation
        # the time array goes from t=0 to t=period -> we have a full orbital cycle
        # (both stars have the same orbital period)
        t = np.linspace(0.0, self.__period, self.__num_t)

        # initialize keplerian orbit (both stars follow the same orbit, and depending on their mass, i.e., K, and omega,
        # we obtain a different radial velocity)
        orbit = KeplerianOrbit(t, self.__period, self.__ecc, self.__t_peri)

        # radial velocity array for each star
        rv1 = orbit.keplerian_orbit(self.__K1, self.__omega1)
        rv2 = orbit.keplerian_orbit(self.__K2, self.__omega2)

        # initialize class SingleFileModifier for each star
        sfm1 = SingleFileModifier(self.__standard_wl, self.__T1, self.__v_rot1)
        sfm2 = SingleFileModifier(self.__standard_wl, self.__T2, self.__v_rot2)

        bf_loop_time = time.time()
        print('TIME BEFORE TIME EVOLUTION LOOP : ', bf_loop_time-start_time)

        # loop for time evolution: we calculate the Doppler shift for each radial vel of the array (and obtain a
        # combined dataframe for each time)
        for i in range(self.__num_t):
            # Doppler shift calculus
            sfm1.doppler_shift(rv1[i])
            sfm2.doppler_shift(rv2[i])

            # save the flux of the dataframe corresponding to each star after the Doppler shift for time_i
            df1_i = sfm1.df['flux'].copy()
            df2_i = sfm2.df['flux'].copy()

            # obtaining the dataframe corresponding to this time (combining both stars)
            df_i = self.__sum_spectra(df1_i, df2_i)

            # finally we add the dataframe for time_i to the general dataframe (each column will be a df
            # in a concrete time_i)
            # column_name_wl = 'wl_time_' + str(i)
            column_name_flux = 'flux_time_' + str(i)
            # self.final_df[column_name_wl] = df_i['wl']
            self.final_df[column_name_flux] = df_i['flux']

    def __sum_spectra(self, df1_i, df2_i, integral_check=False, plot_check=False):
        # print('Combining both fluxes')

        df_i = pd.DataFrame()

        # the wl in the combined df will correspond to the standardized wl
        # self.combined_df['wl'] = self.__standard_wl['wl'].copy()
        df_i['wl'] = self.__standard_wl['wl'].copy()

        # sum both fluxes taking into account the weight of each with R21 = R2/R1
        # self.combined_df['flux'] = self.__df1['flux'] + self.__R21 * self.__R21 * self.__df2['flux']
        df_i['flux'] = df1_i + self.__R21 * self.__R21 * df2_i

        if integral_check:
            print('Calculating flux conservation')
            integral_1 = 0.0
            integral_2 = 0.0
            integral_f = 0.0

            for i in range(len(df1_i)):
                integral_1 += self.__standard_wl['wl'].iloc[i] * df1_i['flux'].iloc[i]

            for i in range(len(df2_i)):
                integral_2 += self.__standard_wl['wl'].iloc[i] * df2_i['flux'].iloc[i]

            for i in range(len(self.final_df)):
                integral_f += self.__standard_wl['wl'].iloc[i] * self.final_df['flux'].iloc[i]

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

            l1, = ax.plot(df1_i['wl'], df1_i['flux'])
            l2, = ax.plot(df2_i['wl'], self.__R21*self.__R21 * df2_i['flux'])
            l3, = ax.plot(self.final_df['wl'], self.final_df['flux'])
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

        return df_i

    def __continuum_normalization(self):
        wave = self.__standard_wl['wl'].values
        flux = self.final_df['flux_time_0'].values

        output = rassine(wave, flux)
        continuum = output['output']['continuum_linear']

        fig, ax = plt.subplots()

        l1, = ax.plot(wave, flux)
        l3, = ax.plot(wave, continuum)

        ax.legend((l1, l3), ('flux', 'continuum linear'), loc='upper right', shadow=False)
        ax.set_xlabel('Wavelength (A)')
        ax.set_ylabel('Flux')
        ax.set_title('Continuum Fitting')
        ax.grid(True)
        plt.show()

        for i in range(self.__num_t):
            column_name_flux = 'flux_time_' + str(i)
            self.final_df[column_name_flux] = self.final_df[column_name_flux].div(continuum)

    def plot(self):
        print('Generating combined spectra plot')

        plt.plot(self.final_df['wl'], self.final_df['flux'])
        plt.xlabel('Wavelength (A)')
        plt.ylabel('Flux')
        plt.title('Combined Spectra')
        plt.show()

    def save_to_file(self, path: str, file_name: str):
        print('Saving to file in the CombinedSpectra folder')
        # save the modified file to a csv in the folder 'NewLibrary'
        self.final_df.to_csv(path + file_name + '.csv', index=False)
        save_time = time.time()
        print('TIME AFTER SAVING FILE : ', save_time - start_time)

