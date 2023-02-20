from DopplerShift_and_Convolution import DopplerShift_and_Convolution as dc
from SL_combination import SL_combination
from NewLibraryCreator import NewLibraryCreator as newlib


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''

FWHM = 0.078  # in A, [A]=Angstrom
sigma = FWHM / 2.35482  # FWHM = 2*sqrt(2*ln2)*sigma

test = newlib('lte02300-5.00-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes2.csv', 2300)
test.range_filter(5198.9, 9601.1)
test.instrumental_convolution(sigma, plot=True)
test.rebinning(plot_check=True, integral_check=True)
test.save_to_file()





