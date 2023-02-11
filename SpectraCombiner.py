import pandas as pd
import math


class SpectraCombiner:

    def __init__(self, T1, T2, R21, L21, inc, v_r1, v_r2, v_rot1, v_rot2):
        # save the introduced variables in class variables
        self.__T1 = T1  # temperature
        self.__T2 = T2
        self.__R21 = R21  # R2/R1 (radius of the stars)
        self.__L21 = L21  # L2/L1 (luminosities of the stars)
        self.__inc = inc  # inclination of the orbital plane
        self.__v_r1 = v_r1  # radial velocity
        self.__v_r2 = v_r2
        self.__v_rot1 = v_rot1  # rotation velocity
        self.__v_rot2 = v_rot2

        # save the data frame with the temperature interpolation for each star
        self.__df1 = self.__temperature_interpolator(self.__T1)
        self.__df2 = self.__temperature_interpolator(self.__T2)

        # Doppler shift
        self.__df1['wl'] = self.__doppler_shift(self.__v_r1)
        self.__df2['wl'] = self.__doppler_shift(self.__v_r2)

        # create the data frame for the combined spectra
        self.__combined_df = None

    def __temperature_interpolator(self, temperature):
        print('Interpolation of Temperatures')
        val = float(temperature) / 100.0
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
        interpolator = (temperature - float(t1)) / (float(t2) - float(t1))

        return df_t1['flux'] + (df_t2['flux'] - df_t1['flux']) * interpolator

    def __doppler_shift(self, radial_vel):
        print('Applying Doppler Shift')
        c = 299792458  # light velocity (m/s)

        # implicit loop
        return (1.0 + float(radial_vel) / float(c)) * self.__df1['wl']  # before the doppler shift,
                                                                        # both df (df1, df2) have the same wl

    def doppler_broadening(self): ...

    def sum_spectra(self): ...

    def flux_factor(self): ...

    def save_to_file(self): ...

