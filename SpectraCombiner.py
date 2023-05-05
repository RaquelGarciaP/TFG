import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import CubicSpline
import time
from SingleFileModifier import SingleFileModifier
from KeplerianOrbit import KeplerianOrbit
from Rassine import rassine

start_time = time.time()


class SpectraCombiner:

    def __init__(self, general_params, orbital_params, num_t, standard_wl, CARMENES_file):

        # save the standard wavelength df (it is an input, so we only read the file one time -in main-)
        self.__standard_wl = standard_wl

        # save the CARMENES file (will be used to save the final flux as a fits file in a format that SERVAL can use)
        self.__CARMENES_file = CARMENES_file

        # general parameters of the stars
        self.__T1, self.__T2, self.__R21, self.__v_rot1, self.__v_rot2 = general_params
        # T: temperature of the star
        # R21 = R2/R1: ratio between the radius of each star
        # v_rot: rotational velocity

        # orbital parameters
        self.__period, self.__K1, self.__K2, self.__ecc, self.__omega1, self.__omega2, self.__t_peri = orbital_params
        # period: orbital period
        # K: radial velocity semi-amplitude
        # ecc: eccentricity of the orbit
        # omega: angle of periastron
        # t_peri: time of periastron_passage

        # number of steps in t array
        self.__num_t = num_t

        # create the data frame for the combined spectra (each column will contain the spectra for a concrete time)
        self.final_df = pd.DataFrame()
        # self.final_df['wave'] = self.__standard_wl['wl'].copy()

        # time evolution (self.final_df will be filled with the combined spectra for each time)
        self.__time_evolution()

        # continuum normalization
        self.__continuum_normalization()

        # save the spectra in a fits file with the CARMENES
        self.__save_to_file()

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
            flux1_i = sfm1.df['flux'].to_numpy()
            flux2_i = sfm2.df['flux'].to_numpy()

            # obtaining the dataframe corresponding to this time (combining both stars)
            flux_i = self.__sum_spectra(flux1_i, flux2_i)

            # finally we add the dataframe for time_i to the general dataframe (each column will be a df
            # in a concrete time_i)
            column_name_flux = 'flux_time_' + str(i)
            self.final_df[column_name_flux] = flux_i

    def __sum_spectra(self, flux1_i, flux2_i, integral_check=False, plot_check=False):
        # print('Combining both fluxes')

        # sum both fluxes taking into account the weight of each with R21 = R2/R1
        final_flux_i = flux1_i + self.__R21 * self.__R21 * flux2_i

        if integral_check:
            print('Calculating flux conservation')
            integral_1 = 0.0
            integral_2 = 0.0
            integral_f = 0.0

            for i in range(len(flux1_i)):
                integral_1 += self.__standard_wl['delta wl'].iloc[i] * flux1_i[i]

            for i in range(len(flux2_i)):
                integral_2 += self.__standard_wl['delta wl'].iloc[i] * flux2_i[i]

            for i in range(len(self.final_df)):
                integral_f += self.__standard_wl['delta wl'].iloc[i] * final_flux_i[i]

            interpol_integral_flux = integral_1 + self.__R21 * self.__R21 * integral_2
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

            l1, = ax.plot(self.__standard_wl['wl'], flux1_i)
            l2, = ax.plot(self.__standard_wl['wl'], self.__R21 * self.__R21 * flux2_i)
            l3, = ax.plot(self.__standard_wl['wl'], final_flux_i)

            ax.legend((l1, l2, l3), ('T1', 'T2', 'Joined Spectra'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Spectra Sum check')
            plt.show()

        # if plot == False: (correct way to express it -> if not plot:)
        else:
            pass

        return final_flux_i

    def __continuum_normalization(self, plot_continuum=False, plot_normalization=False):
        wave = self.__standard_wl['wl'].to_numpy()
        flux = self.final_df['flux_time_0'].to_numpy()

        # call the function RASSINE (returns the continuum of the flux)
        output = rassine(wave, flux)
        # the output of RASSINE has an equidistant grid
        wave_equidistant = output['wave']
        continuum_equidistant = output['output']['continuum_linear']

        # interpolate to obtain the continuum in our standardized grid
        continuum_standard = np.interp(wave, wave_equidistant, continuum_equidistant)

        # loop to normalize the flux for each time (we only need to obtain the continuum for one time bc the change of
        # the continuum along time can be neglected)
        for i in range(self.__num_t):
            column_name_flux = 'flux_time_' + str(i)
            # divide the flux by the continuum -> we obtain the normalized flux
            self.final_df[column_name_flux] = self.final_df[column_name_flux].div(continuum_standard)

        if plot_continuum:
            print('doing continuum plot')
            # plot of the continuum obtained with RASSINE
            fig, ax = plt.subplots()

            l1, = ax.plot(wave, flux)  # ax.plot(output['wave'], output['flux'])
            l2, = ax.plot(wave, continuum_standard)  # ax.plot(output['wave'], continuum_equidistant)

            ax.legend((l1, l2), ('flux', 'continuum linear'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('Continuum Fitting')
            ax.grid(True)
            plt.show()

        else:
            pass

        if plot_normalization:
            print('doing normalization plot')
            # plot of the normalized spectra

            plt.plot(wave, self.final_df['flux_time_0'])
            plt.xlabel('Wavelength (A)')
            plt.ylabel('Flux')
            plt.title('Normalized flux')
            plt.grid(True)
            plt.show()

        else:
            pass

    def plot(self):
        print('Generating combined spectra plot')

        plt.plot(self.__standard_wl['wl'], self.final_df['flux_time_0'])  # todo: mirar com variar aixo amb el GIFcreator.py
        plt.xlabel('Wavelength (A)')
        plt.ylabel('Flux')
        plt.title('Combined Spectra')
        plt.show()

    def __save_to_file(self, integral_check=True):
        print('Saving to fits files')
        # save the modified file to a csv in the folder 'NewLibrary'

        initial_order = 2
        final_order = 53

        wave_phoenix = self.__standard_wl['wl'].to_numpy()

        # make new directory where the fits files will be saved
        directory = 'params'  # directory name
        parent_dir = './CombinedSpectra/'  # parent directory path
        path = os.path.join(parent_dir, directory)  # path
        # os.mkdir(path)  # create the directory

        # time loop
        for i in range(self.__num_t):
            # select the flux corresponding to the time i
            column_name_flux = 'flux_time_' + str(i)
            flux_phoenix = self.final_df[column_name_flux].to_numpy()

            # loop for each of the orders of the CARMENES fits file
            for j in range(final_order - 1):
                # class to interpolate the original sampling (standard)
                f = CubicSpline(wave_phoenix, flux_phoenix)
                # we interpolate to the CARMENES grid and rewrite the original flux for our own in the CARMENES file
                self.__CARMENES_file['SPEC'].data[j+initial_order] = f(self.__CARMENES_file['WAVE'].data[j+initial_order])

            file_name = 'file_time_' + str(i) + '.fits'
            file_path = './CombinedSpectra/params/' + file_name
            # self.__CARMENES_file.writeto(file_path, output_verify='silentfix')

            # self.__CARMENES_file.info()
            # print(self.__CARMENES_file['SPEC'].data[0])

        if integral_check:
            # we do the check in time i=max bc it is assumed that if the flux is conserved for one time, it is for all
            df_copy = self.__standard_wl.copy()

            t_max = self.__num_t - 1  # maximum time
            column_name = 'flux_time_' + str(t_max)
            flux_phoenix_copy = self.final_df[column_name].to_numpy(copy=True)

            df_copy['flux'] = flux_phoenix_copy

            order = 5

            mask = (df_copy['wl'] >= self.__CARMENES_file['WAVE'].data[order][0]) & \
                   (df_copy['wl'] <= self.__CARMENES_file['WAVE'].data[order][4095])
            df_with_mask = df_copy[mask]

            integral_standard = 0.0
            integral_carmenes = 0.0

            # integral of the flux b4 the interpolation with the CARMENES grid
            for i in range(len(df_with_mask)):
                integral_standard += df_with_mask['delta wl'].iloc[i] * df_with_mask['flux'].iloc[i]

            # integral of the flux after the interpolation with the CARMENES grid
            delta_wl = np.empty(len(self.__CARMENES_file['SPEC'].data[order]))
            for i in range(len(self.__CARMENES_file['SPEC'].data[order])):
                if i + 1 == len(self.__CARMENES_file['SPEC'].data[order]):
                    print('he entrat aqui!!')
                    delta_wl[i] = delta_wl[i - 1]
                else:
                    delta_wl[i] = self.__CARMENES_file['SPEC'].data[order][i + 1] - self.__CARMENES_file['SPEC'].data[order][i]

                integral_carmenes += delta_wl[i] * self.__CARMENES_file['SPEC'].data[order][i]

            diff = abs(integral_standard - integral_carmenes)
            print(' Flux integral in standard grid: ', integral_standard)
            print(' Flux integral in CARMENES grid: ', integral_carmenes)
            print(' Difference: ', diff, '   Difference / initial flux: ', diff / integral_standard)

            fig, ax = plt.subplots()

            l1, = ax.plot(df_with_mask['wl'], df_with_mask['flux'])
            l2, = ax.plot(self.__CARMENES_file['WAVE'].data[order], self.__CARMENES_file['SPEC'].data[order])

            ax.legend((l1, l2), ('Initial flux', 'Final flux'), loc='upper right', shadow=False)
            ax.set_xlabel('Wavelength (A)')
            ax.set_ylabel('Flux')
            ax.set_title('CARMENES resampling check')
            plt.show()

        else:
            pass

        save_time = time.time()
        print('TIME AFTER SAVING ALL THE FILES : ', save_time - start_time)

