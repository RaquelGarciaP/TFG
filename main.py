from NewLibraryCreator import NewLibraryCreator as newlib
from SpectraCombiner import SpectraCombiner as sc


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''


'''test = newlib('lte03000-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', 3000)
test.range_filter(5198.9, 9601.1)
test.instrumental_convolution()
test.rebinning(integral_check=True)
test.save_to_file()'''

'''c = 299792458.0

T1, T2 = 2345, 2379
R21 = 2
L21 = 2
v_r1, v_r2 = 1050000.2, 11056.0
v_rot1, v_rot2 = 47.23, 25.9

combination = sc(T1, T2, R21, L21, v_r1, v_r2, v_rot1, v_rot2)
# combination.sum_spectra()
# combination.plot()
# combination.save_to_file()'''





