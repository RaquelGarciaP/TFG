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

# read the CARMENES file (will be used to save the final flux as a fits file in a format that SERVAL can use)
CARMENES_file = fits.open('./NewLibrary/car-20160520T03h10m13s-sci-gtoc-vis_A.fits')

# read the file containing the dates when we have CARMENES measurements (time array)
t_array = np.load('./NewLibrary/CARMENESdates.npy')

# *** general parameters of the stars ***
T1, T2 = 2801.0, 2701.0  # 11854.26, 11567.39
R21 = 0.854005047
v_rot1, v_rot2 = 3000.0, 2900.0

general_params = T1, T2, R21, v_rot1, v_rot2
# T: temperature of the star
# R21 = R2/R1: ratio between the radius of each star
# v_rot: rotational velocity

# *** orbital parameters of the stars ***
period = 15768000.0  # seconds
K1, K2 = 4543.933874, 5302.624869
ecc = 0.0
omega1 = 0.0
omega2 = omega1 + 180.0
t_peri = 0.0

orbital_params = period, K1, K2, ecc, omega1, omega2, t_peri
# ####orbital_params2 = period, K2, ecc, omega2, t_peri
# period: orbital period
# K: radial velocity semi-amplitude
# ecc: eccentricity of the orbit
# omega: angle of periastron
# t_peri: time of periastron_passage

test = SpectraCombiner(general_params, orbital_params, t_array, standard_wl, CARMENES_file)

# close the CARMENES fits file
CARMENES_file.close()

