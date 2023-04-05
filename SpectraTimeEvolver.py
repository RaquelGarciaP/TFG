import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
from SpectraCombiner import SpectraCombiner
from KeplerianOrbit import KeplerianOrbit


class SpectraTimeEvolver:

    def __init__(self, general_params, orbital_params1, orbital_params2):

        # params1, params2: parameters of star 1 and star 2

        self.__num_t = 25  # number of steps in t array
        orbital_period = 301.25

        # time array
        self.__t = np.linspace(0.0, orbital_period, self.__num_t)

        # general parameters of the stars
        self.__T1, self.__T2, self.__R21, self.__v_rot1, self.__v_rot2 = general_params
        # T: temperature of the star
        # R21 = R2/R1: ratio between the radius of each star
        # v_rot: rotational velocity

        # orbital parameters
        period1, K1, ecc1, omega1, t_peri1 = orbital_params1
        period2, K2, ecc2, omega2, t_peri2 = orbital_params2
        # period: orbital period
        # K: radial velocity semi-amplitude
        # ecc: eccentricity of the orbit
        # omega: angle of periastron
        # t_peri: time of periastron_passage

        # initialize keplerian orbit for both stars
        orbit1 = KeplerianOrbit(self.__t, period1, K1, ecc1, omega1, t_peri1)
        orbit2 = KeplerianOrbit(self.__t, period2, K2, ecc2, omega2, t_peri2)

        # radial velocity array of both stars
        self.__rv1 = orbit1.rv.copy()
        self.__rv2 = orbit2.rv.copy()
        print(self.__rv1)
        print(self.__rv2)

        # combined spectra in time_i
        self.__combined_i = pd.DataFrame()

        # time evolution
        self.__time_evolution()

    def __time_evolution(self):
        # first we create a directory (folder) that will contain all the combined spectra for each time

        directory = 'params'  # name of the directory
        parent_dir = './CombinedSpectra/'  # parent directory path
        path = os.path.join(parent_dir, directory)  # path
        # create the directory
        # os.mkdir(path)

        # now we can save the combined spectra for each time inside the directory
        images = []
        # loop to obtain the time evolution of star 1 and 2:
        for i in range(len(self.__t)):
            # initialize class for each time (new t => new rv => new combination)
            comb = SpectraCombiner(self.__T1, self.__T2, self.__R21, self.__rv1[i], self.__rv2[i], self.__v_rot1, self.__v_rot2)
            # copy the combined dataframe in a variable (it's overwritten for a new time_i)
            self.__combined_i = comb.combined_df.copy()

            # plot check
            # comb.plot()

            # save to file
            # file_name = 'time_' + str(i)
            # comb.save_to_file(path, file_name)

            # GIF:
            # Crear lista de imágenes a partir de los datos
            fig, ax = plt.subplots(figsize=(14, 8))
            self.__combined_i.plot(x='wl', y='flux', ax=ax)
            ax.set_title(f'Frame {i}')
            fig.canvas.draw()
            image = np.array(fig.canvas.renderer.buffer_rgba())
            images.append(image)
            plt.close()

        # Guardar lista de imágenes en un archivo .gif
        imageio.mimsave('time_evolution.gif', images, fps=10)

    '''def save_to_folder(self):
        # first we create a directory (folder) that will contain all the combined spectra for each time

        directory = 'params'  # name of the directory
        parent_dir = './CombinedSpectra/'  # parent directory path
        path = os.path.join(parent_dir, directory)  # path
        # create the directory
        os.mkdir(path)

        # now we can save the combined spectra for each time inside the directory'''

