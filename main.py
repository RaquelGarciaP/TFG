from NewLibraryCreator import NewLibraryCreator as newlib
from SpectraCombiner import SpectraCombiner as sc


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''


'''test = newlib('lte11400-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', 11400)
test.range_filter(5199.9, 9600.1)
test.instrumental_convolution(integral_check=True)
test.rebinning(integral_check=True)
test.save_to_file()'''

T1, T2 = 11974.26, 2379
R21 = 2
L21 = 2
v_r1, v_r2 = 105.2, 11056.0
v_rot1, v_rot2 = 207.23, 25.9

combination = sc(T1, T2, R21, L21, v_r1, v_r2, v_rot1, v_rot2)
# combination.sum_spectra()
# combination.plot()
# combination.save_to_file()





