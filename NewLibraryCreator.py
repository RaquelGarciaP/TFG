import pandas as pd


class NewLibraryCreator:

    def __init__(self, file_name):
        # read the file with pandas
        self.__file_name = file_name
        self.__data_frame = pd.read_csv(self.__file_name, names=['wl', 'flux'])
        # create a class variable to save the filtered data frame
        self.__filtered_df = None

    def range_filter(self, rang_value1, rang_value2):

        # create a boolean mask to choose the rows with the desired value
        mask = (self.__data_frame['wl'] >= rang_value1) & (self.__data_frame['wl'] <= rang_value2)

        # choose the rows with the mask
        # self.__filtered_df = self.__data_frame.loc[mask, :]
        self.__filtered_df = self.__data_frame[mask]

    def instrumental_convolution(self): ...


    def save_to_file(self):
        # save the filtered file to a csv
        self.__filtered_df.to_csv(self.__file_name + '_filtered.csv', index=False)


