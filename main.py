from NewLibraryCreator import NewLibraryCreator as newlib
from SpectraCombiner import SpectraCombiner as sc


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''


'''test = newlib('lte02400-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', 2400)
test.range_filter(5199.9, 9600.1)
test.instrumental_convolution(integral_check=True, plot_check=True)
test.rebinning(integral_check=True, plot_check=True)
test.save_to_file()'''

T1, T2 = 11804.26, 11567.39
R21 = 2.67
v_r1, v_r2 = 11530.2, 11680.7
v_rot1, v_rot2 = 2997.23, 3100.39

combination = sc(T1, T2, R21, v_r1, v_r2, v_rot1, v_rot2)
combination.sum_spectra(integral_check=True, plot_check=True)
combination.plot()
# combination.save_to_file()





