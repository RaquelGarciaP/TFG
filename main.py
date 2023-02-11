from DopplerShift_and_Convolution import DopplerShift_and_Convolution as dc
from SL_combination import SL_combination
from NewLibraryCreator import NewLibraryCreator as newlib


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''

test = newlib('prova_data.csv')
test.instrumental_convolution(0.9)
# test.save_to_file()





