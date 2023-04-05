from NewLibraryCreator import NewLibraryCreator as newlib
from SpectraTimeEvolver import SpectraTimeEvolver


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''


'''test = newlib('lte02400-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', 2400)
test.range_filter(5199.9, 9600.1)
test.instrumental_convolution(integral_check=True, plot_check=True)
test.rebinning(integral_check=True, plot_check=True)
test.save_to_file()'''


T1, T2 = 11854.26, 11567.39
R21 = 2.67
v_rot1, v_rot2 = 2997.23, 3100.39

# general parameters of the stars
general_params = T1, T2, R21, v_rot1, v_rot2
# T: temperature of the star
# R21 = R2/R1: ratio between the radius of each star
# v_rot: rotational velocity


period1, period2 = 301.25, 301.25
K1, K2 = 147980.06, 156760.43
ecc1, ecc2 = 0.12, 0.078
omega1 = 52.34
omega2 = omega1 + 180.0
t_peri1, t_peri2 = 3.54, 18.31

# orbital parameters
orbital_params1 = period1, K1, ecc1, omega1, t_peri1
orbital_params2 = period2, K2, ecc2, omega2, t_peri2
# period: orbital period
# K: radial velocity semi-amplitude
# ecc: eccentricity of the orbit
# omega: angle of periastron
# t_peri: time of periastron_passage

test = SpectraTimeEvolver(general_params, orbital_params1, orbital_params2)




