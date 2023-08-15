import numpy as np
import pandas as pd
from astropy.io import fits
from SpectraCombiner import SpectraCombiner
# from NewLibraryCreator import NewLibraryCreator as newlib


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''


'''test = newlib('lte02900-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', 2900)
test.range_filter(5199.9, 9600.1)
test.instrumental_convolution(integral_check=True)
test.rebinning(integral_check=True)
test.save_to_file()'''


# read the standard wavelength file (with CARMENES sampling)
standard_wl = pd.read_csv('./NewLibrary/standard_wl.csv')

# read the file containing the dates when we have CARMENES measurements (time array)
CARMENES_info = pd.read_csv('./CARMENES_data/info_observations.csv')

# *** general parameters of the stars ***
T1, T2 = 2800.0, 2300.0  # K
R21 = 0.97  # radius_2/radius_1
v_rot1, v_rot2 = 50000.0, 40000.0  # m/s

general_params = T1, T2, R21, v_rot1, v_rot2
# T: temperature of the star
# R21 = R2/R1: ratio between the radius of each star
# v_rot: rotational velocity

# *** orbital parameters of the stars ***
period = 182.536  # days
K1, K2 = 1910.14, 2164.83  # m/s
ecc = 0.0
omega1 = 90.0  # degree
omega2 = omega1 + 180.0  # degree
t_peri = period * 0.4  # days (barycentric julian day - 2457000)

orbital_params = period, K1, K2, ecc, omega1, omega2, t_peri
# ####orbital_params2 = period, K2, ecc, omega2, t_peri
# period: orbital period
# K: radial velocity semi-amplitude
# ecc: eccentricity of the orbit
# omega: angle of periastron
# t_peri: time of periastron_passage

# directory name where tha files containing the final data will be saved (inside folder 'CombinedSpectra')
directory_name = 'directory_name'

test = SpectraCombiner(general_params, orbital_params, CARMENES_info, standard_wl, directory_name)
