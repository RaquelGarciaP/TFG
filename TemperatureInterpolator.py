import math
import pandas as pd


class TemperatureInterpolator:

    def __init__(self, temperature, log_g):
        self.__temperature = temperature
        self.__log_g = log_g

        self.__val = float(self.__temperature) / 100.0
        floor = math.floor(self.__val)
        ceil = math.ceil(self.__val)

        # if the introduced temperature is equal to the top or the floor, we choose an already existing file
        if (self.__val == floor) or (self.__val == ceil):

            self.__file_name = 'file_' + str(self.__temperature) + '_' + str(self.__log_g) + '.csv'

            # we read the file using the library pandas
            print('Reading the file')
            self.__initial_df = pd.read_csv(self.__file_name, names=['wl', 'flux'])

        # if the temperature is not equal to the floor or ceil, we do a linear interpolation
        else:
            T1 = int(floor*100)
            T2 = int(ceil*100)
            self.__file_name_T1 = 'file_' + str(T1) + '_' + str(self.__log_g) + '.csv'
            self.__file_name_T2 = 'file_' + str(T2) + '_' + str(self.__log_g) + '.csv'

            self.__data_T1 = pd.read_csv(self.__file_name_T1, names=['wl', 'flux'])
            self.__data_T2 = pd.read_csv(self.__file_name_T2, names=['wl', 'flux'])

    def __linear_interpolation(self, x, x0, y0, x1, y1):
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
