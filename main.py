from DopplerShift_and_Convolution import DopplerShift_and_Convolution as dc
from SL_combination import SL_combination
from FileValueFilter import FileValueFilter as fvf


'''
Per convertir els arxius .dat  a .csv: obrim amb un bloc de notes >> Edición >> Remplazar >> ' ' (espai) por ',' (coma)
'''

mydata = dc(2400, 5.0)

# mydata.doppler_shift(0.2)
mydata.convolution(0.1)
# mydata.do_plot()

# mydata.save_to_file()

# **********************
'''
file1 = 'demofile1.csv'
file2 = 'demofile2.csv'

my_combination = SL_combination(file1, file2)
my_combination.combine_files()'''

# *********************

'''file_filter = fvf('demo_file.csv')
file_filter.apply_filter(5, 10)
file_filter.save_to_file()'''






