


class DopplerShift:

    def __init__(self, radial_vel, data):

        self.__radial_vel = radial_vel
        self.__c = 299792458  # light velocity (m/s)

        self.__data = data  # array with wl values

    def apply_shift(self):
        print('Applying Doppler Shift')
        # loop to apply the Doppler shift:
        for i in range(len(self.__data)):
            self.__data[i] = (1 + float(self.__radial_vel) / float(self.__c)) * self.__data[i]
