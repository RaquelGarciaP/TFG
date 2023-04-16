import pandas as pd
from SpectraCombiner import SpectraCombiner
# from NewLibraryCreator import NewLibraryCreator as newlib
# from SpectraTimeEvolver import SpectraTimeEvolver
# from SingleFileModifier import SingleFileModifier


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''


'''test = newlib('lte02400-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', 2400)
test.range_filter(5199.9, 9600.1)
test.instrumental_convolution(integral_check=True, plot_check=True)
test.rebinning(integral_check=True, plot_check=True)
test.save_to_file()'''


# read the standard wavelength file (with CARMENES sampling)
standard_wl = pd.read_csv('./NewLibrary/standard_wl')

# number of steps in t array (= measures over time)
num_t = 100

# *** general parameters of the stars ***
T1, T2 = 11854.26, 11567.39
R21 = 2.67
v_rot1, v_rot2 = 2997.23, 3100.39

general_params = T1, T2, R21, v_rot1, v_rot2
# T: temperature of the star
# R21 = R2/R1: ratio between the radius of each star
# v_rot: rotational velocity

# *** orbital parameters of the stars ***
period = 1728000.0  # seconds
K1, K2 = 147980.06, 156760.43
ecc = 0.0
omega1 = 52.34
omega2 = omega1 + 180.0
t_peri = 3.54

orbital_params = period, K1, K2, ecc, omega1, omega2, t_peri
# ####orbital_params2 = period, K2, ecc, omega2, t_peri
# period: orbital period
# K: radial velocity semi-amplitude
# ecc: eccentricity of the orbit
# omega: angle of periastron
# t_peri: time of periastron_passage

test = SpectraCombiner(standard_wl, general_params, orbital_params, num_t)
# test.save_to_file('./CombinedSpectra/', 'test_file')




