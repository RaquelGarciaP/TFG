import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


class ContinuumNormalization:

    def __init__(self, df):
        self.__initial_df = df
        self.__continuum = pd.DataFrame()
        self.__normalized_df = pd.DataFrame()

        self.__sigma_clipping()

    def __norm(self, sigma):
        # Create a MinMaxScaler object
        scaler = MinMaxScaler()

        # Normalize the DataFrame
        self.__normalized_df = pd.DataFrame(scaler.fit_transform(self.__initial_df), columns=self.__initial_df.columns)

        # Print the normalized DataFrame
        # print(df_normalized)

    def __sigma_clipping(self):
        # median value of the flux
        median = self.__initial_df['flux'].median()

        # standard deviation calculus
        rest_squared_flux = (self.__initial_df['flux'] - median) * (self.__initial_df['flux'] - median)
        error = rest_squared_flux.sum()

        # standard deviation
        sigma = np.sqrt(error / len(self.__initial_df))
        print(sigma, 3.0*sigma, median)

        # mask
        mask = (self.__initial_df['wl'] >= median-3.0*sigma) & (self.__initial_df['wl'] <= median+3.0*sigma)

        # keep the data that fulfills the mask condition
        self.__continuum = self.__initial_df[mask]

        plt.plot(self.__continuum['wl'], self.__continuum['flux'])
        plt.show()

        # plot
        fig, ax = plt.subplots()

        l1, = ax.plot(self.__initial_df['wl'], self.__initial_df['flux'])
        l2, = ax.plot(self.__continuum['wl'], self.__continuum['flux'])

        ax.legend((l1, l2), ('initial', 'continuum'), loc='upper right', shadow=False)
        ax.set_xlabel('Wavelength (A)')
        ax.set_ylabel('Flux')
        ax.set_title('Normalization')
        plt.show()




